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
import type { FanTaleApi } from "@fantale/api";

export class StoryService {
  private client: FanTaleApi;

  constructor(client: FanTaleApi) {
    this.client = client;
  }

  // Stories
  createStory(body: StoryCreationRequest) {
    return this.client.createStory(body);
  }

  getStoryStatus(story_id: string) {
    return this.client.getStoryStatus(story_id);
  }

  listUserStories(user_id: number) {
    return this.client.listUserStories(user_id);
  }

  getStory(story_id: string) {
    return this.client.getStory(story_id);
  }

  getChapter(story_id: string, chapter_id: number) {
    return this.client.getChapter(story_id, chapter_id);
  }

  submitChapterFeedback(
    story_id: string,
    chapter_id: number,
    feedback_text: string,
    like: boolean
  ) {
    return this.client.submitChapterFeedback(story_id, chapter_id, feedback_text, like);
  }

  shareStory(story_id: string) {
    return this.client.shareStory(story_id);
  }

  listFandoms() {
    return this.client.listFandoms();
  }
}
