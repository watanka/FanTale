"use client";
import { useFandoms } from "../../features/stories/hooks";

export default function FandomsPage() {
  const { data, isLoading, isError, error } = useFandoms();

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold tracking-tight">팬덤</h2>
      {isLoading && <div className="text-sm text-black/60 dark:text-neutral-400">불러오는 중...</div>}
      {isError && (
        <div className="text-sm text-red-600">불러오기 실패: {(error as any)?.message}</div>
      )}
      {data && (
        <ul className="divide-y divide-black/10 rounded-md border border-black/10 bg-white dark:divide-white/10 dark:border-white/10 dark:bg-neutral-900">
          {data.fandoms.length === 0 ? (
            <li className="p-4 text-sm text-black/60 dark:text-neutral-400">표시할 팬덤이 없습니다.</li>
          ) : (
            data.fandoms.map((f) => (
              <li key={f.story_id} className="p-4">
                <div className="flex items-center gap-4">
                  <div className="h-12 w-12 flex-shrink-0 rounded-md bg-gradient-to-br from-brand-main/30 to-brand-purple/30" />
                  <div>
                    <div className="font-medium">{f.title}</div>
                    <div className="text-xs text-black/60 dark:text-neutral-400">챕터 {f.chapters?.length ?? 0}개</div>
                  </div>
                </div>
              </li>
            ))
          )}
        </ul>
      )}
    </div>
  );
}
