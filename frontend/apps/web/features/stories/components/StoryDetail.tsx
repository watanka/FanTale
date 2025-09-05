"use client";
import { useState } from "react";
import type { StoryRetrieveResponse } from "@fantale/types";
import { useSubmitFeedback } from "../hooks";

export function StoryDetail({
  storyId,
  data,
}: {
  storyId: number;
  data: StoryRetrieveResponse;
}) {
  const [feedbacks, setFeedbacks] = useState<Record<number, { text: string; like: boolean }>>({});
  const feedbackMutation = useSubmitFeedback();

  return (
    <section className="rounded-lg bg-white p-6 shadow-card">
      <h3 className="text-lg font-semibold">완성된 이야기</h3>
      <p className="mt-1 text-sm text-black/60">총 {data.chapters.length}개의 챕터</p>

      <div className="mt-4 space-y-6">
        {data.chapters.map((ch) => (
          <article key={ch.chapter_id} className="rounded-md border border-black/10 p-4">
            <header className="mb-2">
              <div className="text-xs text-black/60">Chapter {ch.chapter_number}</div>
              <h4 className="text-base font-semibold">{ch.chapter_name}</h4>
              <p className="mt-1 text-sm text-black/60">{ch.summary}</p>
            </header>
            <div className="prose max-w-none whitespace-pre-wrap text-sm leading-6">
              {ch.content}
            </div>
            <div className="mt-4 border-t border-black/10 pt-4">
              <h5 className="text-sm font-medium">피드백 남기기</h5>
              <div className="mt-2 grid grid-cols-1 gap-2 sm:grid-cols-3">
                <textarea
                  value={feedbacks[ch.chapter_id]?.text || ""}
                  onChange={(e) =>
                    setFeedbacks((prev) => ({
                      ...prev,
                      [ch.chapter_id]: {
                        text: e.target.value,
                        like: prev[ch.chapter_id]?.like ?? true,
                      },
                    }))
                  }
                  placeholder="느낀 점을 자유롭게 적어주세요"
                  className="sm:col-span-2 min-h-[60px] w-full rounded-md border border-black/10 px-3 py-2"
                />
                <div className="flex items-start gap-3">
                  <label className="inline-flex items-center gap-2 text-sm">
                    <input
                      type="checkbox"
                      checked={feedbacks[ch.chapter_id]?.like ?? true}
                      onChange={(e) =>
                        setFeedbacks((prev) => ({
                          ...prev,
                          [ch.chapter_id]: {
                            text: prev[ch.chapter_id]?.text || "",
                            like: e.target.checked,
                          },
                        }))
                      }
                    />
                    좋았어요
                  </label>
                  <button
                    onClick={() =>
                      feedbackMutation.mutate({
                        storyId,
                        chapterId: ch.chapter_id,
                        feedback_text: feedbacks[ch.chapter_id]?.text || "",
                        like: feedbacks[ch.chapter_id]?.like ?? true,
                      })
                    }
                    className="ml-auto inline-flex items-center rounded-md bg-[color:var(--color-brand-main)] px-3 py-2 text-sm font-medium text-black hover:opacity-90"
                  >
                    제출
                  </button>
                </div>
              </div>
              {feedbackMutation.isPending && (
                <div className="mt-2 text-xs text-black/50">제출 중...</div>
              )}
              {feedbackMutation.isError && (
                <div className="mt-2 text-xs text-red-600">제출 실패: {(feedbackMutation.error as any)?.message}</div>
              )}
              {feedbackMutation.isSuccess && (
                <div className="mt-2 text-xs text-emerald-600">감사합니다! 피드백이 반영됐어요.</div>
              )}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
