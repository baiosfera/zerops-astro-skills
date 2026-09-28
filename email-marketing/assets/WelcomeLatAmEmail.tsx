import * as React from "react";
import {
  Html,
  Head,
  Body,
  Container,
  Section,
  Row,
  Column,
  Text,
  Heading,
  Button,
  Hr,
  Link,
  Preview,
  Tailwind,
  pixelBasedPreset
} from "@react-email/components";

export interface WelcomeLatAmEmailProps {
  userName?: string;
  discountCode?: string;
  discountValue?: string;
  shopUrl?: string;
  unsubscribeUrl?: string;
}

export const WelcomeLatAmEmail: React.FC<WelcomeLatAmEmailProps> = ({
  userName = "Amigo",
  discountCode = "BIENVENIDO10",
  discountValue = "10%",
  shopUrl = "https://mitienda.com",
  unsubscribeUrl = "https://mitienda.com/api/unsubscribe"
}) => {
  return (
    <Html lang="es" dir="ltr">
      <Head />
      <Preview>Bienvenido a la comunidad. Tu cupón de {discountValue} está listo para ti.</Preview>
      <Tailwind
        config={{
          presets: [pixelBasedPreset],
          theme: {
            extend: {
              colors: {
                brandDark: "#0b0f19",
                brandGold: "#d4af37",
                brandText: "#1f2937"
              }
            }
          }
        }}
      >
        <Body className="bg-[#f3f4f6] font-sans py-8">
          <Container className="max-w-[580px] mx-auto bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
            <Section className="bg-brandDark px-8 py-6 text-center">
              <Text className="text-brandGold tracking-widest uppercase text-xs font-semibold m-0">
                BAIOSFERA • GENTLE COMMERCE
              </Text>
            </Section>

            <Section className="px-8 pt-8 pb-6">
              <Heading className="text-2xl font-bold text-brandText m-0 mb-3">
                ¡Hola, {userName}! 👋
              </Heading>
              <Text className="text-base text-gray-700 leading-relaxed m-0 mb-4">
                Nos alegra darte la bienvenida. Tienes un <strong>{discountValue} de descuento</strong> en tu primera compra con el cupón:
              </Text>

              <Section className="bg-gray-50 border border-dashed border-gray-300 rounded-lg p-4 text-center mb-6">
                <Text className="text-xl font-mono font-bold text-brandDark tracking-wider m-0">{discountCode}</Text>
              </Section>

              <Section className="text-center mb-6">
                <Button href={shopUrl} className="bg-brandDark text-brandGold font-semibold px-8 py-3.5 rounded-lg text-sm">
                  Explorar Catálogo →
                </Button>
              </Section>

              <Section className="border-t border-gray-100 pt-5 mt-6">
                <Row className="text-center">
                  <Column className="w-1/3">
                    <Text className="text-xs font-bold text-gray-800 m-0">🇨🇴 Envíos Colombia</Text>
                    <Text className="text-[11px] text-gray-500 m-0">Servientrega / Coordinadora</Text>
                  </Column>
                  <Column className="w-1/3">
                    <Text className="text-xs font-bold text-gray-800 m-0">💳 Pagos Seguros</Text>
                    <Text className="text-[11px] text-gray-500 m-0">PSE • Nequi • Bancolombia</Text>
                  </Column>
                  <Column className="w-1/3">
                    <Text className="text-xs font-bold text-gray-800 m-0">🛡️ Garantía Total</Text>
                    <Text className="text-[11px] text-gray-500 m-0">Soporte WhatsApp</Text>
                  </Column>
                </Row>
              </Section>
            </Section>

            <Hr className="border-gray-200 m-0" />
            <Section className="bg-gray-50 px-8 py-6 text-center">
              <Text className="text-xs text-gray-500 m-0">
                <Link href={unsubscribeUrl} className="text-gray-500 underline">
                  Cancelar suscripción
                </Link>
              </Text>
            </Section>
          </Container>
        </Body>
      </Tailwind>
    </Html>
  );
};
