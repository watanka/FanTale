"use client";

export default function MePage() {
  // TODO: Replace with real user profile once auth is ready
  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold tracking-tight">내 정보</h2>
      <section className="rounded-md border border-black/10 bg-white p-4 dark:border-white/10 dark:bg-neutral-900">
        <div className="mb-3 h-24 w-full rounded-md bg-gradient-to-r from-brand-pink/30 via-brand-main/30 to-brand-purple/30" />
        <div className="text-sm text-black/60 dark:text-neutral-400">베타 버전</div>
        <div className="mt-1">간단한 프로필과 설정이 이곳에 표시됩니다.</div>
      </section>
    </div>
  );
}
