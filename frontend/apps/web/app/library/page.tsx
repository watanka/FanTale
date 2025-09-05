"use client";
import Link from "next/link";
import { useState } from "react";
import { useUserStories } from "../../features/stories/hooks";

export default function LibraryPage() {
  // TODO: replace with real auth user id
  const [userId] = useState<number>(1);
  const { data, isLoading, isError, error } = useUserStories(userId);

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold tracking-tight">내 서재</h2>
      {isLoading && <div className="text-sm text-black/60">불러오는 중...</div>}
      {isError && (
        <div className="text-sm text-red-600">불러오기 실패: {(error as any)?.message}</div>
      )}
      {data && (
        <ul className="divide-y divide-black/10 rounded-md border border-black/10 bg-white dark:divide-white/10 dark:border-white/10 dark:bg-neutral-900">
          {data.stories.length === 0 ? (
            <li className="p-4 text-sm text-black/60 dark:text-neutral-400">아직 생성된 이야기가 없습니다.</li>
          ) : (
            data.stories.map((s) => (
              <li key={s.story_id} className="p-4 hover:bg-black/[0.03] dark:hover:bg-white/5">
                <Link className="flex items-center justify-between" href={`/library/${s.story_id}`}>
                  <div className="flex items-center gap-3">
                    <div className="h-10 w-10 flex-shrink-0 rounded-md bg-gradient-to-br from-brand-main/30 to-brand-purple/30" />
                    <div>
                      <div className="font-medium">{s.title || `Story #${s.story_id}`}</div>
                      <div className="text-xs text-black/60 dark:text-neutral-400">챕터 {s.chapters?.length ?? 0}개</div>
                      {s.summary && (
                        <div className="mt-0.5 line-clamp-1 text-xs text-black/60 dark:text-neutral-400">{s.summary}</div>
                      )}
                    </div>
                  </div>
                  <span className="text-xs text-black/50 dark:text-white/50">보기 →</span>
                </Link>
              </li>
            ))
          )}
        </ul>
      )}
    </div>
  );
}
