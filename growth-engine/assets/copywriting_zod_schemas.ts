import { z } from "zod";

export const PillarContentInputSchema = z.object({
  id: z.string().uuid(),
  title: z.string().min(5).max(150),
  coreTheme: z.string().min(10),
  targetAudience: z.object({
    role: z.string(),
    industry: z.string(),
    primaryPainPoint: z.string(),
    dreamOutcome: z.string(),
    marketRegion: z.enum(["Colombia", "LatAm_General"]).default("Colombia")
  }),
  framework: z.enum(["HOOK_STORY_OFFER", "STORYBRAND_SB7", "HORMOZI_VALUE", "PASTOR"]),
  keyInsights: z.array(z.string()).min(3).max(7),
  epiphanyStory: z.object({
    lowPoint: z.string(),
    breakthroughMoment: z.string(),
    tangibleResult: z.string()
  }),
  primaryOffer: z.object({
    name: z.string(),
    dreamOutcome: z.string(),
    quickWinTimeframe: z.string(),
    riskReversalGuarantee: z.string(),
    ctaText: z.string(),
    ctaUrlOrKeyword: z.string(),
    priceCopOrUsd: z.string().optional()
  })
});

export const OmnichannelAtomizationBundleSchema = z.object({
  pillarId: z.string().uuid(),
  whatsapp: z.object({
    broadcastMessage: z.object({
      hookOpening: z.string().max(120),
      storySnippet: z.string().max(350),
      clearValueDelivery: z.string().max(250),
      conversationalCta: z.string().max(120)
    }),
    oneOnOneChatFlow: z.object({
      icebreaker: z.string(),
      qualificationQuestion: z.string(),
      objectionBusterTrust: z.string(),
      paymentLinkIntro: z.string()
    })
  }),
  email: z.object({
    subjectLineOptions: z.array(z.string().min(5).max(70)).length(3),
    previewText: z.string().min(10).max(100),
    salutation: z.string().default("Hola, {{first_name}}"),
    heroHook: z.string(),
    amplifiedPainStory: z.string(),
    frameworkLesson: z.array(z.string()).min(2),
    offerPitch: z.object({
      headline: z.string(),
      bulletBenefits: z.array(z.string()).min(3),
      riskReversal: z.string(),
      directCtaButtonText: z.string(),
      directCtaUrl: z.string().url()
    }),
    postScriptum: z.string()
  }),
  xThread: z.object({
    hookTweet: z.string().max(280),
    bodyTweets: z.array(z.string().max(280)).min(4).max(8),
    summaryTweet: z.string().max(280),
    ctaTweet: z.string().max(280)
  }),
  linkedinCarousel: z.object({
    postCaption: z.string().min(50).max(1500),
    slides: z.array(
      z.object({
        slideNumber: z.number().int(),
        title: z.string().max(50),
        mainBody: z.string().max(180),
        visualNote: z.string()
      })
    ).min(5).max(10),
    closingSlideCta: z.string()
  }),
  shortVideo: z.object({
    videoLengthSeconds: z.number().int().min(15).max(60),
    soundtrackRecommendation: z.string(),
    timelineBlocks: z.object({
      hook0to3s: z.object({
        spokenWords: z.string().max(25),
        onScreenText: z.string().max(45),
        visualAction: z.string()
      }),
      story4to30s: z.object({
        spokenWords: z.string(),
        bRollSuggestions: z.array(z.string()),
        subtitlesKeyHighlights: z.array(z.string())
      }),
      offer30to50s: z.object({
        spokenWords: z.string(),
        onScreenOfferText: z.string(),
        riskReversalCallout: z.string()
      }),
      cta50to60s: z.object({
        spokenWords: z.string(),
        onScreenCtaAnimation: z.string()
      })
    })
  })
});

export type PillarContentInput = z.infer<typeof PillarContentInputSchema>;
export type OmnichannelAtomizationBundle = z.infer<typeof OmnichannelAtomizationBundleSchema>;
