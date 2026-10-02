export interface ShippingAddress {
  recipientName: string;
  streetLine1: string;
  streetLine2?: string;
  city: string;
  stateOrProvince: string;
  postalCode?: string;
  countryCode: string; // ISO 3166-1 alpha-2 (e.g. US, CO, MX, ES)
  phoneNumber: string;
  divipolaCode?: string; // Optional Colombian DANE 8-digit code
}

export interface ParcelDimensions {
  weightKg: number;
  lengthCm: number;
  widthCm: number;
  heightCm: number;
}

export interface ShippingRateQuote {
  carrierId: string;
  carrierName: string;
  serviceLevel: string;
  estimatedDeliveryDays: number;
  rate: number;
  currency: string;
  guaranteedDelivery: boolean;
}

export interface WaybillGenerationResult {
  carrierId: string;
  trackingNumber: string;
  labelUrl: string;
  format: "PDF" | "ZPL" | "PNG";
  dispatchedAt: string;
}

export interface IShippingCarrierProvider {
  readonly carrierId: string;
  calculateRates(
    origin: ShippingAddress,
    destination: ShippingAddress,
    parcel: ParcelDimensions
  ): Promise<ShippingRateQuote[]>;

  generateWaybill(
    orderId: string,
    origin: ShippingAddress,
    destination: ShippingAddress,
    parcel: ParcelDimensions
  ): Promise<WaybillGenerationResult>;

  trackShipment(trackingNumber: string): Promise<{
    trackingNumber: string;
    status: "PENDING" | "IN_TRANSIT" | "OUT_FOR_DELIVERY" | "DELIVERED" | "RETURNED";
    updatedAt: string;
    history: Array<{ status: string; timestamp: string; location?: string }>;
  }>;
}

export class StandardCarrierProvider implements IShippingCarrierProvider {
  readonly carrierId = "standard-global";

  async calculateRates(
    origin: ShippingAddress,
    destination: ShippingAddress,
    parcel: ParcelDimensions
  ): Promise<ShippingRateQuote[]> {
    const baseRate = origin.countryCode === destination.countryCode ? 5.0 : 25.0;
    const weightSurcharge = parcel.weightKg * 2.5;

    return [
      {
        carrierId: this.carrierId,
        carrierName: "Standard Express",
        serviceLevel: "STANDARD",
        estimatedDeliveryDays: 3,
        rate: Number((baseRate + weightSurcharge).toFixed(2)),
        currency: "USD",
        guaranteedDelivery: false,
      },
      {
        carrierId: this.carrierId,
        carrierName: "Priority Overnight",
        serviceLevel: "EXPRESS",
        estimatedDeliveryDays: 1,
        rate: Number(((baseRate + weightSurcharge) * 2.2).toFixed(2)),
        currency: "USD",
        guaranteedDelivery: true,
      },
    ];
  }

  async generateWaybill(
    orderId: string,
    origin: ShippingAddress,
    destination: ShippingAddress,
    parcel: ParcelDimensions
  ): Promise<WaybillGenerationResult> {
    const trackingNumber = `TRK-${Date.now()}-${Math.floor(Math.random() * 10000)}`;
    return {
      carrierId: this.carrierId,
      trackingNumber,
      labelUrl: `https://shipping.example.com/labels/${trackingNumber}.pdf`,
      format: "PDF",
      dispatchedAt: new Date().toISOString(),
    };
  }

  async trackShipment(trackingNumber: string) {
    return {
      trackingNumber,
      status: "IN_TRANSIT" as const,
      updatedAt: new Date().toISOString(),
      history: [
        { status: "Shipment Created", timestamp: new Date().toISOString() },
        { status: "Package Received at Sort Facility", timestamp: new Date().toISOString() },
      ],
    };
  }
}
