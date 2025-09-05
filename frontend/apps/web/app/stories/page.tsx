"use client";
import { useState } from "react";
import { StoryForm } from "@/features/stories/components/StoryForm";
import { StoryStatus } from "@/features/stories/components/StoryStatus";
import { StoryDetail } from "@/features/stories/components/StoryDetail";
import { useCreateStory, useStory, useStoryStatus } from "@/features/stories/hooks";

export default function StoriesPage() {
  const [storyId, setStoryId] = useState<number | null>(null);

  const createMutation = useCreateStory();
  const statusQuery = useStoryStatus(storyId);
  const ready = statusQuery.data?.status === "READY";
  const pending = statusQuery.data?.status === "PENDING" || createMutation.isPending;
  const storyQuery = useStory(storyId, ready);

  return (
    <div className="space-y-6">
      <StoryForm
        pending={createMutation.isPending}
        onSubmit={(values) =>
          createMutation.mutate(values, {
            onSuccess: (data) => setStoryId(data.story_id),
          })
        }
      />

      {storyId && (
        <StoryStatus
          storyId={storyId}
          status={statusQuery.data?.status || (createMutation.isSuccess ? "PENDING" : undefined)}
          pending={pending}
        />
      )}

      {ready && storyQuery.data && (
        <StoryDetail storyId={storyId as number} data={storyQuery.data} />
      )}
    </div>
  );
}
