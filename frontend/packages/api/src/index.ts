import type {
  StoryCreationRequest,
  StoryCreateResponse,
  StoryStatusResponse,
  StoryListResponse,
  StoryRetrieveResponse,
  StoryChapterRetrieveResponse,
  ChapterFeedbackResponse,
  StoryShareResponse,
  FandomListResponse,
} from "@fantale/types";

export type ClientOptions = {
  baseUrl?: string;
  getToken?: () => Promise<string | null> | string | null;
};

function resolveBaseUrl(opts?: ClientOptions) {
  if (opts?.baseUrl) return opts.baseUrl;
  const envBase =
    (typeof process !== "undefined" &&
      (process.env.NEXT_PUBLIC_API_BASE_URL || process.env.EXPO_PUBLIC_API_BASE_URL)) ||
    "";
  if (envBase) return envBase;
  const isBrowser = typeof window !== "undefined";
  // In browser with Next.js rewrites, call relative "/api"
  return isBrowser ? "/api" : "http://127.0.0.1:8000";
}

async function request<T>(
  path: string,
  init: RequestInit = {},
  opts?: ClientOptions
): Promise<T> {
  const baseUrl = resolveBaseUrl(opts);
  const token = typeof opts?.getToken === "function" ? await opts!.getToken!() : null;
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(init.headers || {}),
  };
  if (token) (headers as any)["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${baseUrl}${path}`, {
    ...init,
    headers,
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`HTTP ${res.status}: ${text || res.statusText}`);
  }
  return (await res.json()) as T;
}

export function createClient(options?: ClientOptions) {
  return {
    // Stories
    createStory: (body: StoryCreationRequest) =>
      request<StoryCreateResponse>("/stories", {
        method: "POST",
        body: JSON.stringify(body),
      }, options),

    getStoryStatus: (story_id: string) =>
      request<StoryStatusResponse>(`/stories/${story_id}/status`, {}, options),

    listUserStories: (user_id: number) =>
      request<StoryListResponse>(`/users/stories?user_id=${user_id}`, {}, options),

    getStory: (story_id: string) =>
      request<StoryRetrieveResponse>(`/stories/${story_id}`, {}, options),

    getChapter: (story_id: string, chapter_id: number) =>
      request<StoryChapterRetrieveResponse>(
        `/stories/${story_id}/chapter/${chapter_id}`,
        {},
        options
      ),

    submitChapterFeedback: (
      story_id: string,
      chapter_id: number,
      feedback_text: string,
      like: boolean
    ) =>
      request<ChapterFeedbackResponse>(
        `/stories/${story_id}/chapter/${chapter_id}/feedback?feedback_text=${encodeURIComponent(
          feedback_text
        )}&like=${like}`,
        { method: "POST" },
        options
      ),

    shareStory: (story_id: string) =>
      request<StoryShareResponse>(`/stories/${story_id}/share`, { method: "POST" }, options),

    listFandoms: () => request<FandomListResponse>(`/fandoms`, {}, options),
  };
}

export type FanTaleApi = ReturnType<typeof createClient>;
