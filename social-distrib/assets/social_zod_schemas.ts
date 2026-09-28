import { z } from "zod";

export const InstagramPublishSchema = z.object({
  igUserId: z.string().min(1),
  accessToken: z.string().min(1),
  caption: z.string().max(2200).optional(),
  shareToFeed: z.boolean().default(true),
  media: z.discriminatedUnion("type", [
    z.object({
      type: z.literal("IMAGE"),
      imageUrl: z.string().url(),
      altText: z.string().max(1000).optional()
    }),
    z.object({
      type: z.literal("REELS"),
      videoUrl: z.string().url(),
      coverUrl: z.string().url().optional()
    }),
    z.object({
      type: z.literal("CAROUSEL"),
      items: z.array(
        z.object({
          mediaType: z.enum(["IMAGE", "VIDEO"]),
          url: z.string().url()
        })
      ).min(2).max(10)
    })
  ])
});

export const TikTokPublishSchema = z.object({
  userAccessToken: z.string().min(1),
  title: z.string().max(2200).default(""),
  privacyLevel: z.enum(["PUBLIC_TO_EVERYONE", "MUTUAL_FOLLOW_FRIENDS", "SELF_ONLY"]).default("PUBLIC_TO_EVERYONE"),
  videoUrl: z.string().url()
});

export const LinkedInPublishSchema = z.object({
  accessToken: z.string().min(1),
  authorUrn: z.string().regex(/^urn:li:(organization|person):[0-9]+$/),
  commentary: z.string().max(3000),
  visibility: z.enum(["PUBLIC", "CONNECTIONS"]).default("PUBLIC"),
  documentPdfUrl: z.string().url().optional(),
  documentTitle: z.string().optional()
});

export const XPublishSchema = z.object({
  userBearerToken: z.string().min(1),
  text: z.string().max(280),
  replyToTweetId: z.string().optional()
});
