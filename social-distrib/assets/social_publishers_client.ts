import {
  InstagramPublishSchema,
  TikTokPublishSchema,
  LinkedInPublishSchema,
  XPublishSchema
} from "./social_zod_schemas";
import { z } from "zod";

export async function publishToInstagram(input: z.infer<typeof InstagramPublishSchema>): Promise<string> {
  const data = InstagramPublishSchema.parse(input);

  // 1. Crear contenedor
  const containerRes = await fetch(`https://graph.instagram.com/v26.0/${data.igUserId}/media`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${data.accessToken}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      media_type: data.media.type,
      video_url: data.media.type === "REELS" ? data.media.videoUrl : undefined,
      image_url: data.media.type === "IMAGE" ? data.media.imageUrl : undefined,
      caption: data.caption,
      share_to_feed: data.shareToFeed
    })
  });

  const { id: containerId } = await containerRes.json();

  // 2. Polling hasta FINISHED
  let status = "IN_PROGRESS";
  let attempts = 0;
  while (status === "IN_PROGRESS" && attempts < 20) {
    await new Promise((r) => setTimeout(r, 10000));
    const statusRes = await fetch(`https://graph.instagram.com/v26.0/${containerId}?fields=status_code`, {
      headers: { "Authorization": `Bearer ${data.accessToken}` }
    });
    const statusJson = await statusRes.json();
    status = statusJson.status_code;
    attempts++;
  }

  if (status !== "FINISHED") throw new Error(`IG Container failed with status: ${status}`);

  // 3. Publicar
  const pubRes = await fetch(`https://graph.instagram.com/v26.0/${data.igUserId}/media_publish`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${data.accessToken}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ creation_id: containerId })
  });

  const { id: mediaId } = await pubRes.json();
  return mediaId;
}

export async function publishToX(input: z.infer<typeof XPublishSchema>): Promise<string> {
  const data = XPublishSchema.parse(input);

  const res = await fetch("https://api.twitter.com/2/tweets", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${data.userBearerToken}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      text: data.text,
      reply: data.replyToTweetId ? { in_reply_to_tweet_id: data.replyToTweetId } : undefined
    })
  });

  const json = await res.json();
  return json.data?.id || "tweet_published";
}
