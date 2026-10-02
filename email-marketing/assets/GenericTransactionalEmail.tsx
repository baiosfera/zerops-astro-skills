import * as React from "react";
import {
  Html,
  Head,
  Body,
  Container,
  Section,
  Text,
  Heading,
  Button,
  Hr,
  Link,
  Preview,
  Tailwind,
  pixelBasedPreset
} from "@react-email/components";

export interface GenericTransactionalEmailProps {
  brandName?: string;
  userName?: string;
  previewText?: string;
  headline?: string;
  bodyText?: string;
  actionText?: string;
  actionUrl?: string;
  footerNote?: string;
  unsubscribeUrl?: string;
  primaryColor?: string;
}

export const GenericTransactionalEmail: React.FC<GenericTransactionalEmailProps> = ({
  brandName = "Platform",
  userName = "Valued Customer",
  previewText = "Important update regarding your account",
  headline = "Action Required: Update Details",
  bodyText = "Thank you for partnering with us. Your account environment is ready and awaiting configuration.",
  actionText = "Get Started",
  actionUrl = "https://example.com/dashboard",
  footerNote = "This is an automated operational notification.",
  unsubscribeUrl = "https://example.com/unsubscribe",
  primaryColor = "#2563eb"
}) => {
  return (
    <Html lang="en" dir="ltr">
      <Head />
      <Preview>{previewText}</Preview>
      <Tailwind
        config={{
          presets: [pixelBasedPreset],
          theme: {
            extend: {
              colors: {
                brandPrimary: primaryColor,
                brandDark: "#0f172a",
                brandGray: "#64748b",
                brandLight: "#f8fafc"
              }
            }
          }
        }}
      >
        <Body className="bg-brandLight font-sans text-brandDark p-4">
          <Container className="max-w-[580px] mx-auto bg-white rounded-lg border border-solid border-slate-200 p-8 shadow-sm">
            <Section className="mb-6">
              <Text className="text-xl font-bold tracking-tight text-brandDark uppercase m-0">
                {brandName}
              </Text>
            </Section>

            <Heading className="text-2xl font-semibold text-brandDark mb-4">
              {headline}
            </Heading>

            <Text className="text-base text-slate-700 leading-relaxed mb-4">
              Hello {userName},
            </Text>

            <Text className="text-base text-slate-700 leading-relaxed mb-6">
              {bodyText}
            </Text>

            {actionUrl && (
              <Section className="text-center my-6">
                <Button
                  className="bg-brandPrimary text-white font-medium text-sm py-3 px-6 rounded-md no-underline inline-block"
                  href={actionUrl}
                >
                  {actionText}
                </Button>
              </Section>
            )}

            <Hr className="border-slate-200 my-6" />

            <Section className="text-xs text-brandGray leading-5">
              <Text className="m-0 mb-2">{footerNote}</Text>
              {unsubscribeUrl && (
                <Text className="m-0">
                  If you no longer wish to receive these emails, you may{" "}
                  <Link href={unsubscribeUrl} className="text-brandPrimary underline">
                    unsubscribe here
                  </Link>.
                </Text>
              )}
            </Section>
          </Container>
        </Body>
      </Tailwind>
    </Html>
  );
};

export default GenericTransactionalEmail;
