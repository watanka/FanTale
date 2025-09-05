export type StoryParameter = {
    num_chapters: number;
    idols: string;
    genre: string;
};
export type StoryCreationRequest = {
    user_id: number;
    story_parameter: StoryParameter;
};
export type StoryListRequest = {
    user_id: number;
};
export type StoryRetrieveRequest = {
    story_id: number;
};
export type ChapterRetrieveRequest = {
    chapter_id: number;
};
export type ChapterFeedbackRequest = {
    chapter_id: number;
    feedback_text: string;
    like: boolean;
};
export type Chapter = {
    chapter_id: number;
    chapter_number: number;
    title: string;
    summary: string;
    content: string;
};
export type Story = {
    story_id: number;
    title: string;
    chapters: Chapter[];
};
export type StoryCreateResponse = {
    story_id: number;
    status: string;
};
export type StoryStatusResponse = {
    status: string;
};
export type StoryListResponse = {
    stories: Story[];
};
export type StoryRetrieveResponse = {
    story_id: number;
    title: string;
    chapters: Chapter[];
};
export type StoryChapterRetrieveResponse = {
    chapter: Chapter;
};
export type ChapterFeedbackResponse = {
    chapter_id: number;
    feedback: string;
};
export type StoryShareResponse = {
    story_id: number;
};
export type FandomListResponse = {
    fandoms: Story[];
};
