"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";

export default function GoogleCallbackPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const code = searchParams.get("code");
    if (!code) {
      setError("Google 인증 코드가 없습니다.");
      return;
    }

    const run = async () => {
      try {
        const resp = await fetch(
          `/api/auth/google/callback?code=${encodeURIComponent(code)}`,
          { credentials: "include" }
        );
        const data = await resp.json();
        if (!resp.ok || (data && data.error)) {
          setError(data?.detail || data?.error || "로그인에 실패했습니다.");
          return;
        }
        // Store tokens and user info
        localStorage.setItem("fantale_auth", JSON.stringify(data));
        // Notify other components (e.g., NavBar) that auth state changed
        try {
          window.dispatchEvent(new Event("fantale-auth-updated"));
        } catch {}
        // Go to homepage
        router.replace("/");
      } catch (e) {
        setError("네트워크 오류가 발생했습니다.");
      }
    };

    run();
  }, [searchParams, router]);

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold tracking-tight">구글 로그인</h2>
      {error ? (
        <div className="rounded-md border border-red-200 bg-red-50 p-3 text-sm text-red-700">
          오류: {error}
        </div>
      ) : (
        <div className="text-sm text-black/70 dark:text-neutral-300">로그인 처리중…</div>
      )}
    </div>
  );
}
