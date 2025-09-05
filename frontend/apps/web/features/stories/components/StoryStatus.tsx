"use client";

export function StoryStatus({
  storyId,
  status,
  pending,
}: {
  storyId: number;
  status?: string;
  pending?: boolean;
}) {
  return (
    <section className="rounded-lg bg-white p-6 shadow-card">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">진행 상태</h3>
        <span className="text-sm text-black/60">Story ID: {storyId}</span>
      </div>
      <div className="mt-3 text-sm">
        상태: <span className="font-medium">{status || "-"}</span>
      </div>
      {pending && (
        <div className="mt-2 text-xs text-black/50">챕터를 생성 중입니다. 잠시만 기다려 주세요...</div>
      )}
    </section>
  );
}
