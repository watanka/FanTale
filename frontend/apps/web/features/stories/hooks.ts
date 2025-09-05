"use client";
import { useMutation, useQuery } from "@tanstack/react-query";
import type {
  StoryCreateResponse,
  StoryStatusResponse,
  StoryRetrieveResponse,
  StoryListResponse,
  StoryChapterRetrieveResponse,
  ChapterFeedbackResponse,
  FandomListResponse,
} from "@fantale/types";
import { api } from "../../lib/api";
import { StoryService } from "./service";

const service = new StoryService(api);

export function useCreateStory() {
  return useMutation({
    mutationFn: async (vars: {
      userId: number;
      idols: string;
      genre: string;
      numChapters: number;
    }): Promise<StoryCreateResponse> => {
      return service.createStory({
        user_id: vars.userId,
        story_parameter: {
          idols: vars.idols,
          genre: vars.genre,
          num_chapters: vars.numChapters,
        },
      });
    },
  });
}

export function useStoryStatus(storyId: string | null) {
  return useQuery<StoryStatusResponse>({
    queryKey: ["story-status", storyId],
    queryFn: async () => service.getStoryStatus(storyId as string),
    enabled: !!storyId,
    refetchInterval: (query) =>
      query.state.data?.status === "PENDING" ? 1500 : false,
  });
}

export function useStory(storyId: string | null, enabled = true) {
  return useQuery<StoryRetrieveResponse>({
    queryKey: ["story", storyId],
    queryFn: async () => service.getStory(storyId as string),
    enabled: !!storyId && enabled,
  });
}

export function useSubmitFeedback() {
  return useMutation({
    mutationFn: async (vars: {
      storyId: string;
      chapterId: number;
      feedback_text: string;
      like: boolean;
    }): Promise<ChapterFeedbackResponse> => {
      const { storyId, chapterId, feedback_text, like } = vars;
      return service.submitChapterFeedback(storyId, chapterId, feedback_text, like);
    },
  });
}

export function useUserStories(userId: number | null) {
  return useQuery<StoryListResponse>({
    queryKey: ["stories", userId],
    queryFn: async () => service.listUserStories(userId as number),
    enabled: !!userId,
  });
}

export function useChapter(storyId: string | null, chapterId: number | null) {
  return useQuery<StoryChapterRetrieveResponse>({
    queryKey: ["chapter", storyId, chapterId],
    queryFn: async () => service.getChapter(storyId as string, chapterId as number),
    enabled: !!storyId && !!chapterId,
  });
}

export function useFandoms() {
  return useQuery<FandomListResponse>({
    queryKey: ["fandoms"],
    queryFn: async () => service.listFandoms(),
  });
}
