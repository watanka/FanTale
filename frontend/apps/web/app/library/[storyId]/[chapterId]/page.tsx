"use client";
import { useParams } from "next/navigation";
import Link from "next/link";
import { useState } from "react";
import { useChapter } from "../../../../features/stories/hooks";

export default function ChapterPage() {
  const params = useParams();
  const storyId = (params?.storyId as string) ?? null;
  const chapterId = Number(params?.chapterId);
  const { data, isLoading, isError, error } = useChapter(
    storyId,
    chapterId
  );

  // Reader controls
  const [fontSize, setFontSize] = useState<number>(16);
  const [lineHeight, setLineHeight] = useState<number>(1.7);

  const fmtKST = (iso: string) => {
    try {
      const d = new Date(iso);
      return new Intl.DateTimeFormat("ko-KR", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        hour12: false,
        timeZone: "Asia/Seoul",
      }).format(d);
    } catch {
      return iso;
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold tracking-tight">챕터</h2>
        <Link className="text-sm text-[color:var(--color-brand-main)] hover:underline" href={`/library/${storyId}`}>
          ← 챕터 목록으로
        </Link>
      </div>
      {isLoading && <div className="text-sm text-black/60">불러오는 중...</div>}
      {isError && (
        <div className="text-sm text-red-600">불러오기 실패: {(error as any)?.message}</div>
      )}
      {data && (
        <article className="rounded-md border border-black/10 bg-white p-5 dark:border-white/10 dark:bg-neutral-900">
          <header className="mb-2">
            <div className="text-xs text-black/60">Chapter {data.chapter.chapter_number}</div>
            <h3 className="text-lg font-semibold">{data.chapter.chapter_name}</h3>
            <p className="mt-1 text-sm text-black/60 dark:text-neutral-400">{data.chapter.summary}</p>
            {(() => {
              const iso = data.chapter.available_from;
              const available = iso ? new Date(iso) : null;
              const locked = false; // available ? available.getTime() > Date.now() : false;
              return locked ? (
                <div className="mt-2 inline-flex items-center gap-2 rounded-full bg-yellow-50 px-3 py-1 text-xs text-yellow-800 ring-1 ring-yellow-200">
                  <span className="font-medium">미리보기</span>
                  <span>공개 예정: {fmtKST(iso!)} (KST)</span>
                </div>
              ) : null;
            })()}
          </header>
          <div className="mb-4 aspect-video w-full overflow-hidden rounded-md bg-gradient-to-br from-brand-main/25 via-brand-pink/20 to-brand-purple/25" />
          <div className="mb-3 flex flex-wrap items-center gap-3 text-xs text-black/60 dark:text-white/60">
            <span className="hidden sm:inline">가독성</span>
            <div className="inline-flex items-center overflow-hidden rounded-full border border-black/10 bg-white/70 shadow-sm dark:border-white/10 dark:bg-neutral-800">
              <button
                type="button"
                onClick={() => setFontSize((v) => Math.max(14, v - 1))}
                className="px-3 py-1.5 hover:bg-black/[0.04] dark:hover:bg-white/5"
                aria-label="글자 작게"
              >
                A-
              </button>
              <div className="px-2 text-[11px] opacity-70">{fontSize}px</div>
              <button
                type="button"
                onClick={() => setFontSize((v) => Math.min(22, v + 1))}
                className="px-3 py-1.5 hover:bg-black/[0.04] dark:hover:bg-white/5"
                aria-label="글자 크게"
              >
                A+
              </button>
            </div>
            <div className="inline-flex items-center overflow-hidden rounded-full border border-black/10 bg-white/70 shadow-sm dark:border-white/10 dark:bg-neutral-800">
              <button
                type="button"
                onClick={() => setLineHeight((v) => Math.max(1.2, parseFloat((v - 0.1).toFixed(1))))}
                className="px-3 py-1.5 hover:bg-black/[0.04] dark:hover:bg-white/5"
                aria-label="줄간격 줄이기"
              >
                –
              </button>
              <div className="px-2 text-[11px] opacity-70">{lineHeight.toFixed(1)}</div>
              <button
                type="button"
                onClick={() => setLineHeight((v) => Math.min(2.0, parseFloat((v + 0.1).toFixed(1))))}
                className="px-3 py-1.5 hover:bg-black/[0.04] dark:hover:bg-white/5"
                aria-label="줄간격 늘리기"
              >
                +
              </button>
            </div>
          </div>
          {(() => {
            const iso = data.chapter.available_from;
            const available = iso ? new Date(iso) : null;
            const locked = false; // available ? available.getTime() > Date.now() : false;
            const baseClass = "prose prose-neutral dark:prose-invert max-w-none whitespace-pre-wrap";
            const blurClass = locked
              ? " select-none pointer-events-none blur-sm md:blur-md"
              : "";
            return (
              <div className="relative">
                <div
                  className={baseClass + blurClass}
                  style={{ fontSize: `${fontSize}px`, lineHeight: lineHeight as any }}
                >
                  {data.chapter.content}
                </div>
                {locked && (
                  <div className="absolute inset-0 flex flex-col items-center justify-center gap-1 bg-white/60 p-4 text-center text-black/80 backdrop-blur-sm">
                    <div className="text-sm font-semibold">미리보기</div>
                    <div className="text-xs">공개 예정: {fmtKST(iso!)} (KST)</div>
                    <div className="mt-1 text-[11px] text-black/60">공개 이후에 열람하실 수 있어요</div>
                  </div>
                )}
              </div>
            );
          })()}
        </article>
      )}
    </div>
  );
}
