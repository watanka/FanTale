"use client";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useStory } from "../../../features/stories/hooks";

export default function StoryDetailPage() {
  const params = useParams();
  const storyId = (params?.storyId as string) ?? null;
  const { data, isLoading, isError, error } = useStory(storyId, true);

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
      <h2 className="text-2xl font-bold tracking-tight">이야기 상세</h2>
      {isLoading && <div className="text-sm text-black/60 dark:text-neutral-400">불러오는 중...</div>}
      {isError && (
        <div className="text-sm text-red-600">불러오기 실패: {(error as any)?.message}</div>
      )}
      {data && (
        <div className="rounded-md border border-black/10 bg-white p-4 dark:border-white/10 dark:bg-neutral-900">
          <div className="mb-2 text-sm text-black/60 dark:text-neutral-400">Story ID: {data.story_id}</div>
          <h3 className="text-lg font-semibold">{data.title || `Story #${data.story_id}`}</h3>
          {data.summary && (
            <p className="mt-1 text-sm text-black/70 dark:text-neutral-300">{data.summary}</p>
          )}
          <div className="mt-3 mb-4 aspect-video w-full overflow-hidden rounded-md bg-gradient-to-br from-brand-main/25 via-brand-pink/20 to-brand-purple/25" />
          <ul className="mt-4 divide-y divide-black/10 dark:divide-white/10">
            {data.chapters.map((ch) => {
              const available = ch.available_from ? new Date(ch.available_from) : null;
              const locked = available ? available.getTime() > Date.now() : false;
              return (
                <li key={ch.chapter_id} className="py-3">
                  <Link className="flex items-center justify-between hover:underline" href={`/library/${data.story_id}/${ch.chapter_id}`}>
                    <div className="flex items-center gap-3">
                      <div className="h-10 w-10 flex-shrink-0 rounded-md bg-gradient-to-br from-brand-main/30 to-brand-purple/30" />
                      <div>
                        <div className="font-medium">Chapter {ch.chapter_number}. {ch.chapter_name}</div>
                        <div className="text-xs text-black/60 dark:text-neutral-400 line-clamp-1">{ch.summary}</div>
                      </div>
                    </div>
                    {locked ? (
                      <span className="text-xs text-black/50 dark:text-white/50">
                        미공개 • 공개 예정: {fmtKST(ch.available_from!)} (KST)
                      </span>
                    ) : (
                      <span className="text-xs text-black/50 dark:text-white/50">읽기 →</span>
                    )}
                  </Link>
                </li>
              );
            })}
          </ul>
        </div>
      )}
    </div>
  );
}
