/** 2C: Q&A-Kurzfassung im Backend von arsnova v1.3.0 mit 640 Ausgabetoken. */
import { it, expect } from 'vitest';
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import * as S from '@arsnova/shared-types';
import {
  packModerationPromptContext,
  canonicalModerationPromptJson as canon,
} from './moderationPromptContextPacking';
import {
  QA_SUMMARY_MODERATION_PACKING_PROFILE as original,
  prepareModerationSummaryContextFromAnalysis as baseline,
  assemblePreparedModerationSummaryContext as assemble,
  resolveQaSummaryAdapterPlan,
} from './moderationSummaryContext';
import { resetOpenWeightLlmClientForTests } from './openWeightLlmClient';
import { runPreparedQaSummary } from './qaSummaryRuntimeAdapter';
import { bindQaSummaryModelOutputV2 as bind } from './qaSummaryValidateV2';

// Festes Datum für die Testdaten. performance.now() misst die verstrichene Zeit in Millisekunden.
const dir = process.env.EVIDENCE!,
  now = new Date('2026-01-15T10:05:00Z'),
  profile = {
    ...original,
    modelProfile: 'qwen3-4b-instruct-2507-q4_k_m:ctx-8192:study',
    contextWindowTokens: 8192,
  };
const save = (name: string, obj: any) =>
  writeFileSync(dir + '/' + name, JSON.stringify(obj, null, 2) + '\n');
const hash = (s: string) => createHash('sha256').update(s).digest('hex');
const trials: any[] = [];
const url = 'http://127.0.0.1:8080';
const plain = (q: any) => ({ id: q.id, text: q.content.text });

// 1. S6 enthält sechs Referenzfragen, S100 zusätzlich 94 synthetische Fragen.
function fixture(n: number) {
  const f: any = structuredClone(S.MODERATION_PROMPT_CONTEXT_REFERENCE_FIXTURE_V1),
    c = f.context;
  const topics = [
    'Können wir den Regressionskoeffizienten für Datensatz X gemeinsam berechnen?',
    'Ist Aufgabe X aus Kapitel 4 für die Klausur relevant?',
    'Gilt die Anwesenheitspflicht auch für das Tutorium in Woche X?',
  ];
  for (let i = 6; i < n; i++) {
    const id = 'qa-question:eeeeeeee-eeee-4eee-8eee-' + String(i + 1).padStart(12, '0');
    c.sources.push({
      id,
      kind: 'qa-question',
      content: {
        state: 'included',
        text: topics[(i - 6) % 3].replace('X', String(1 + Math.floor((i - 6) / 3))),
        truncated: false,
      },
    });
    c.questions.items.push({
      sourceId: id,
      status: 'ACTIVE',
      answerState: { state: 'unaddressed' },
      votes: { state: 'unavailable', reason: 'not-collected' },
      nlp: { state: 'disabled', reason: 'Nicht erhoben' },
      topicSourceIds: [],
    });
  }
  for (const k of Object.keys(c.questions.corpus)) c.questions.corpus[k] = n;
  c.representation = 'analysis-candidates';
  return S.ModerationAnalysisContextV1Schema.parse({
    schemaVersion: f.schemaVersion,
    contractVersion: S.MODERATION_ANALYSIS_CONTEXT_CONTRACT_VERSION,
    assembledAt: now.toISOString(),
    context: c,
  });
}
const plan = {
  ...resolveQaSummaryAdapterPlan(),
  selectedMode: 'full-context' as const,
  inferenceConfigured: true,
  fallback: null,
};
// 2. A enthält die vom Packer ausgewählten Fragen samt Metadaten, B nur dieselben Texte und IDs.
function prepare(n: number) {
  const analysis = fixture(n),
    packed = packModerationPromptContext({ analysis, profile, packedAt: now }),
    prep = assemble({ promptContext: packed, plan, cache: 'miss' });
  const visible = packed.context.sources
    .filter((s: any) => s.kind === 'qa-question' && s.content.state === 'included')
    .map(plain);
  // Separat berechnen, wie viele Texte bei 7.424 Eingabeeinheiten Platz hätten.
  const all = analysis.context.sources
    .filter((s: any) => s.kind === 'qa-question' && s.content.state === 'included')
    .map(plain);
  const ids = new Set(visible.map((q) => q.id));
  const order = [...visible, ...all.filter((q) => !ids.has(q.id))];
  const cost = (qs: any[]) =>
    Buffer.byteLength(canon(qs)) + packed.budget.instructionTokens + packed.budget.definitionTokens;
  let refill = 0;
  for (let i = 1; i <= order.length && cost(order.slice(0, i)) <= 7424; i++) refill = i;
  return {
    analysis,
    packed,
    prep,
    visible,
    capacity: {
      n,
      visible: visible.length,
      allQuestionTexts: all.length,
      refillBudgetAlone: refill,
      refillWithSelectionLimit: Math.min(refill, analysis.context.scope.selectionLimits.questions),
      bInputByteEstimate: cost(visible),
    },
  };
}
it('controlled recorded summary experiment', async () => {
  // 3. Quellenauswahl bei 4.096 und 8.192 Token vergleichen. Modellläufe verwenden 8.192.
  const cases = new Map([6, 100].map((n) => [n, prepare(n)]));
  const capacities: any[] = [];
  for (const [n, d] of cases) {
    const standard = baseline({ analysis: d.analysis, plan, packedAt: now });
    capacities.push({
      ...d.capacity,
      release4096: standard.request.promptContext.budget,
      release4096Ids: standard.request.promptContext.context.sources.map((s) => s.id),
      budget: d.packed.budget,
    });
    save('fixture-' + n + '.json', d.analysis);
    save('context-' + n + '-A.json', d.packed);
    save('context-' + n + '-B.json', d.visible);
  }
  save('capacity.json', capacities);
  // 4. Quellen-IDs prüfen. Auch eine falsche Aussage kann eine gültige ID haben.
  const six = cases.get(6)!;
  const ok = six.visible[0].id;
  const checks = [
    ['unknown', 'Die Frage ist offen.', ['qa-question:unknown']],
    ['mixed', 'Beispiel.', [ok, 'qa-question:unknown']],
    ['false-semantic', 'Alle 200 Studierenden haben die Regression verstanden.', [ok]],
  ].map(([label, text, ids]) => {
    const output = {
      status: 'ready',
      statements: [{ text, sourceIds: ids }],
      limitations: [],
      suggestedNextSteps: [],
    };
    const out = bind({
      output: S.QaSummaryModelOutputV2Schema.parse(output),
      prepared: six.prep,
      execution: { attemptedMode: 'full-context', effectiveMode: 'full-context', fallback: null },
      analyzedAt: now.toISOString(),
    });
    return {
      label,
      output,
      status: out.status,
      statements: out.statements,
      limitations: out.limitations,
    };
  });
  expect(checks.map((c) => c.status)).toEqual(['uncertain', 'ready', 'ready']);
  save('controls.json', checks);
  if (process.env.ONLY_PACK === '1') return;
  const token = process.env.STUDY_TOKEN!,
    auth = { authorization: 'Bearer ' + token };
  const abort = Date.now() + 720000;
  // 5. Einen Modellaufruf messen und das Backend-Ergebnis speichern.
  async function run(n: number, arm: string, rep: number) {
    const id = (rep === 0 ? 'P' : 'R') + rep + '-S' + n + '-' + arm,
      d = cases.get(n)!;
    if (Date.now() > abort) throw Error('12 minute study deadline');
    if (existsSync(dir + '/' + id + '.json')) throw Error('Existing run ' + id);
    // Vor jedem Lauf den Eingabecache leeren. Das Modell bleibt geladen.
    const erase = await fetch(url + '/slots/0?action=erase', {
      method: 'POST',
      headers: auth,
      signal: AbortSignal.timeout(5000),
    });
    if (!erase.ok) throw Error('Cannot clear slot ' + erase.status + ' ' + (await erase.text()));
    const t0 = performance.now(),
      rec: any = { id, n, arm, rep, fixtureSha256: hash(canon(d.analysis)), kvErased: true };
    const pp = assemble({
      promptContext: packModerationPromptContext({ analysis: d.analysis, profile, packedAt: now }),
      plan,
      cache: 'miss',
    });
    rec.packMs = performance.now() - t0;
    resetOpenWeightLlmClientForTests({
      request: async (input) => {
        if (input.method === 'GET') {
          const s = await fetch(url + input.path, { headers: input.headers, signal: input.signal });
          return { status: s.status, body: await s.text() };
        }
        const b = JSON.parse(input.body!);
        if (arm === 'B') b.messages[2].content = canon(d.visible);
        b.stream = true;
        b.stream_options = { include_usage: true };
        b.seed = 456;
        b.cache_prompt = false;
        rec.wireSha256 = hash(JSON.stringify(b));
        save('request-' + n + '-' + arm + '.json', b);
        const start = performance.now();
        rec.rawContent = '';
        const http = await fetch(url + input.path, {
          method: 'POST',
          headers: input.headers,
          body: JSON.stringify(b),
          signal: input.signal,
        });
        rec.http = http.status;
        if (!http.ok) {
          rec.transportError = await http.text();
          return { status: http.status, body: rec.transportError };
        }
        let buf = '';
        const decoder = new TextDecoder();
        for await (const chunk of http.body!) {
          buf += decoder.decode(chunk, { stream: true });
          let at;
          while ((at = buf.indexOf('\n')) >= 0) {
            const ln = buf.slice(0, at).trim();
            buf = buf.slice(at + 1);
            if (!ln.startsWith('data:') || ln.includes('[DONE]')) continue;
            const e = JSON.parse(ln.slice(5));
            if (e.usage) rec.usage = e.usage;
            if (e.timings) rec.timings = e.timings;
            const ch = e.choices?.[0];
            if (ch?.finish_reason) rec.finish = ch.finish_reason;
            // TTFT: Zeit von der Anfrage bis zum ersten Textfragment.
            if (ch?.delta?.content) {
              rec.ttftMs ??= performance.now() - start;
              rec.rawContent += ch.delta.content;
            }
          }
        }
        rec.requestMs = performance.now() - start;
        return {
          status: http.status,
          body: JSON.stringify({
            model: b.model,
            choices: [{ message: { content: rec.rawContent }, finish_reason: rec.finish }],
            usage: rec.usage,
            timings: rec.timings,
          }),
        };
      },
    });
    try {
      const got = await runPreparedQaSummary(pp);
      rec.execution = got.execution;
      rec.adapterOutput = got.output;
      // Für generierten Text in B sind nur die mitgesendeten Quellen-IDs zulässig.
      const allowed = new Set(d.visible.map((q) => q.id));
      const scoped =
        arm === 'B' && got.execution.effectiveMode === 'full-context'
          ? {
              ...pp,
              request: {
                ...pp.request,
                promptContext: {
                  ...d.packed,
                  context: {
                    ...d.packed.context,
                    sources: d.packed.context.sources.filter((s) => allowed.has(s.id)),
                  },
                },
              },
            }
          : pp;
      // `bound` enthält die geprüfte Kurzfassung oder den extraktiven Ersatz.
      rec.bound = bind({
        output: got.output,
        prepared: scoped,
        execution: got.execution,
        analyzedAt: now.toISOString(),
      });
    } catch (e) {
      rec.error = String(e);
    }
    rec.componentMs = performance.now() - t0;
    rec.stamp = new Date().toISOString();
    for (const [key, file] of Object.entries({
      cgroupBytes: '/sys/fs/cgroup/memory.current',
      cpuStat: '/sys/fs/cgroup/cpu.stat',
    }))
      if (existsSync(file)) rec[key] = readFileSync(file, 'utf8').trim();
    save(id + '.json', rec);
    trials.push(rec);
    console.log(
      id,
      rec.http,
      rec.usage?.prompt_tokens,
      Math.round(rec.componentMs),
      rec.bound?.status,
    );
    if (!rep && rec.http !== 200) throw Error('Pilot transport failed; inspect saved run ' + id);
  }
  // 6. Zwei Aufwärmläufe, danach 20 Messläufe in wechselnder Reihenfolge.
  await run(100, 'A', 0);
  await run(100, 'B', 0);
  for (let rep = 1; rep <= 5; rep++) {
    for (const n of rep % 2 ? [6, 100] : [100, 6])
      for (const arm of (rep + (n === 6 ? 0 : 1)) % 2 ? ['A', 'B'] : ['B', 'A'])
        await run(n, arm, rep);
  }
  expect(trials).toHaveLength(22);
}, 750000);
