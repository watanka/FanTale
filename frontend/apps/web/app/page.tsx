"use client";
import { useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import type {
  StoryCreateResponse,
  StoryRetrieveResponse,
  StoryStatusResponse,
} from "@fantale/types";
import { api } from "../lib/api";

export default function Page() {
  const [userId, setUserId] = useState<number>(1);
  const [idols, setIdols] = useState<string>("카리나");
  const [genre, setGenre] = useState<string>("로맨스");
  const [numChapters, setNumChapters] = useState<number>(10);
  const [storyId, setStoryId] = useState<number | null>(null);

  const createMutation = useMutation({
    mutationFn: async (): Promise<StoryCreateResponse> => {
      return api.createStory({
        user_id: userId,
        story_parameter: {
          idols,
          genre,
          num_chapters: numChapters,
        },
      });
    },
    onSuccess: (data) => {
      setStoryId(data.story_id);
    },
  });

  const statusQuery = useQuery<StoryStatusResponse>({
    queryKey: ["story-status", storyId],
    queryFn: async () => api.getStoryStatus(storyId as number),
    enabled: !!storyId,
    refetchInterval: (query) =>
      query.state.data?.status === "PENDING" ? 1500 : false,
  });

  const storyQuery = useQuery<StoryRetrieveResponse>({
    queryKey: ["story", storyId],
    queryFn: async () => api.getStory(storyId as number),
    enabled: !!storyId && statusQuery.data?.status === "READY",
  });

  const [feedbacks, setFeedbacks] = useState<Record<number, { text: string; like: boolean }>>({});
  const feedbackMutation = useMutation({
    mutationFn: async ({ chapterId }: { chapterId: number }) => {
      const f = feedbacks[chapterId];
      return api.submitChapterFeedback(storyId as number, chapterId, f?.text || "", !!f?.like);
    },
  });

  const onCreate = (e: React.FormEvent) => {
    e.preventDefault();
    if (!idols || !genre || !numChapters) return;
    createMutation.mutate();
  };

  const ready = statusQuery.data?.status === "READY";
  const pending = statusQuery.data?.status === "PENDING" || createMutation.isPending;

  return (
    <div className="space-y-6">
      <section className="rounded-lg border border-black/10 bg-white p-6 shadow-card dark:border-white/10 dark:bg-neutral-900">
        <h2 className="text-2xl font-bold tracking-tight">이야기 생성</h2>
        <form onSubmit={onCreate} className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div className="space-y-1">
            <label className="text-sm font-medium">User ID (dummy)</label>
            <input
              type="number"
              value={userId}
              onChange={(e) => setUserId(parseInt(e.target.value || "1", 10))}
              className="w-full rounded-md border border-black/10 px-3 py-2 dark:border-white/10 dark:bg-neutral-800 dark:text-white"
              min={1}
            />
          </div>
          <div className="space-y-1">
            <label className="text-sm font-medium">최애 (Idols)</label>
            <input
              value={idols}
              onChange={(e) => setIdols(e.target.value)}
              placeholder="예: Karina"
              className="w-full rounded-md border border-black/10 px-3 py-2 dark:border-white/10 dark:bg-neutral-800 dark:text-white"
            />
          </div>
          <div className="space-y-1">
            <label className="text-sm font-medium">장르</label>
            <input
              value={genre}
              onChange={(e) => setGenre(e.target.value)}
              placeholder="예: 로맨스 판타지"
              className="w-full rounded-md border border-black/10 px-3 py-2 dark:border-white/10 dark:bg-neutral-800 dark:text-white"
            />
          </div>
          <div className="space-y-1">
            <label className="text-sm font-medium">챕터 수</label>
            <input
              type="number"
              value={numChapters}
              onChange={(e) => setNumChapters(Math.max(1, Math.min(50, parseInt(e.target.value || "1", 10))))}
              min={1}
              max={50}
              className="w-full rounded-md border border-black/10 px-3 py-2 dark:border-white/10 dark:bg-neutral-800 dark:text-white"
            />
          </div>
          <div className="sm:col-span-2">
            <button
              type="submit"
              disabled={createMutation.isPending}
              className="inline-flex items-center rounded-md bg-[color:var(--color-brand-purple)] px-4 py-2 text-white hover:opacity-90 disabled:opacity-50"
            >
              {createMutation.isPending ? "생성 중..." : "이야기 생성"}
            </button>
          </div>
        </form>
        {createMutation.isError && (
          <p className="mt-3 text-sm text-red-600">생성 실패: {(createMutation.error as any)?.message}</p>
        )}
      </section>

      {storyId && (
        <section className="rounded-lg border border-black/10 bg-white p-6 shadow-card dark:border-white/10 dark:bg-neutral-900">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold">진행 상태</h3>
            <span className="text-sm text-black/60 dark:text-neutral-400">Story ID: {storyId}</span>
          </div>
          <div className="mt-3 text-sm">
            상태: <span className="font-medium">{statusQuery.data?.status || (createMutation.isSuccess ? "PENDING" : "-")}</span>
          </div>
          {pending && (
            <div className="mt-2 text-xs text-black/50 dark:text-white/50">챕터를 생성 중입니다. 잠시만 기다려 주세요...</div>
          )}
        </section>
      )}

      {ready && storyQuery.data && (
        <section className="rounded-lg border border-black/10 bg-white p-6 shadow-card dark:border-white/10 dark:bg-neutral-900">
          <h3 className="text-lg font-semibold">완성된 이야기</h3>
          <p className="mt-1 text-sm text-black/60 dark:text-neutral-400">총 {storyQuery.data.chapters.length}개의 챕터</p>

          <div className="mt-4 space-y-6">
            {storyQuery.data.chapters.map((ch: StoryRetrieveResponse["chapters"][number]) => (
              <article key={ch.chapter_id} className="rounded-md border border-black/10 p-4 dark:border-white/10 dark:bg-neutral-900">
                <header className="mb-2">
                  <div className="text-xs text-black/60 dark:text-neutral-400">Chapter {ch.chapter_number}</div>
                  <h4 className="text-base font-semibold">{ch.chapter_name}</h4>
                  <p className="mt-1 text-sm text-black/60 dark:text-neutral-400">{ch.summary}</p>
                </header>
                <div className="prose prose-neutral dark:prose-invert max-w-none whitespace-pre-wrap text-sm leading-6">
                  {ch.content}
                </div>
                <div className="mt-4 border-t border-black/10 pt-4 dark:border-white/10">
                  <h5 className="text-sm font-medium">피드백 남기기</h5>
                  <div className="mt-2 grid grid-cols-1 gap-2 sm:grid-cols-3">
                    <textarea
                      value={feedbacks[ch.chapter_id]?.text || ""}
                      onChange={(e) =>
                        setFeedbacks((prev) => ({
                          ...prev,
                          [ch.chapter_id]: { text: e.target.value, like: prev[ch.chapter_id]?.like ?? true },
                        }))
                      }
                      placeholder="느낀 점을 자유롭게 적어주세요"
                      className="sm:col-span-2 min-h-[60px] w-full rounded-md border border-black/10 px-3 py-2 dark:border-white/10 dark:bg-neutral-800 dark:text-white"
                    />
                    <div className="flex items-start gap-3">
                      <label className="inline-flex items-center gap-2 text-sm">
                        <input
                          type="checkbox"
                          checked={feedbacks[ch.chapter_id]?.like ?? true}
                          onChange={(e) =>
                            setFeedbacks((prev) => ({
                              ...prev,
                              [ch.chapter_id]: { text: prev[ch.chapter_id]?.text || "", like: e.target.checked },
                            }))
                          }
                        />
                        좋았어요
                      </label>
                      <button
                        onClick={() => feedbackMutation.mutate({ chapterId: ch.chapter_id })}
                        className="ml-auto inline-flex items-center rounded-md bg-[color:var(--color-brand-main)] px-3 py-2 text-sm font-medium text-black hover:opacity-90"
                      >
                        제출
                      </button>
                    </div>
                  </div>
                  {feedbackMutation.isPending && (
                    <div className="mt-2 text-xs text-black/50 dark:text-white/50">제출 중...</div>
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
      )}
    </div>
  );
}
