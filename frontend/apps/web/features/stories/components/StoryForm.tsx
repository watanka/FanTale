"use client";
import { useState } from "react";

export type StoryFormValues = {
  userId: number;
  idols: string;
  genre: string;
  numChapters: number;
};

export function StoryForm({
  initialValues = { userId: 1, idols: "", genre: "", numChapters: 3 },
  pending = false,
  onSubmit,
}: {
  initialValues?: StoryFormValues;
  pending?: boolean;
  onSubmit: (values: StoryFormValues) => void;
}) {
  const [values, setValues] = useState<StoryFormValues>(initialValues);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!values.idols || !values.genre || !values.numChapters) return;
    onSubmit(values);
  };

  return (
    <section className="rounded-lg bg-white p-6 shadow-card">
      <h2 className="text-2xl font-bold tracking-tight">이야기 생성</h2>
      <form onSubmit={handleSubmit} className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div className="space-y-1">
          <label className="text-sm font-medium">User ID (dummy)</label>
          <input
            type="number"
            value={values.userId}
            onChange={(e) =>
              setValues((v) => ({ ...v, userId: parseInt(e.target.value || "1", 10) }))
            }
            className="w-full rounded-md border border-black/10 px-3 py-2"
            min={1}
          />
        </div>
        <div className="space-y-1">
          <label className="text-sm font-medium">최애 (Idols)</label>
          <input
            value={values.idols}
            onChange={(e) => setValues((v) => ({ ...v, idols: e.target.value }))}
            placeholder="예: Karina"
            className="w-full rounded-md border border-black/10 px-3 py-2"
          />
        </div>
        <div className="space-y-1">
          <label className="text-sm font-medium">장르</label>
          <input
            value={values.genre}
            onChange={(e) => setValues((v) => ({ ...v, genre: e.target.value }))}
            placeholder="예: 로맨스 판타지"
            className="w-full rounded-md border border-black/10 px-3 py-2"
          />
        </div>
        <div className="space-y-1">
          <label className="text-sm font-medium">챕터 수</label>
          <input
            type="number"
            value={values.numChapters}
            onChange={(e) =>
              setValues((v) => ({
                ...v,
                numChapters: Math.max(1, Math.min(50, parseInt(e.target.value || "1", 10))),
              }))
            }
            min={1}
            max={50}
            className="w-full rounded-md border border-black/10 px-3 py-2"
          />
        </div>
        <div className="sm:col-span-2">
          <button
            type="submit"
            disabled={pending}
            className="inline-flex items-center rounded-md bg-[color:var(--color-brand-purple)] px-4 py-2 text-white hover:opacity-90 disabled:opacity-50"
          >
            {pending ? "생성 중..." : "이야기 생성"}
          </button>
        </div>
      </form>
    </section>
  );
}
