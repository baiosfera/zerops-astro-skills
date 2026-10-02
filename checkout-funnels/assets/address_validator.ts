export interface RawAddressInput {
  countryCode: string; // ISO 3166-1 alpha-2
  stateOrProvince: string;
  city: string;
  streetLine1: string;
  streetLine2?: string;
  postalCode?: string;
  divipolaCode?: string;
}

export interface NormalizedAddress {
  isValid: boolean;
  standardizedCountry: string;
  standardizedState: string;
  standardizedCity: string;
  standardizedStreet: string;
  postalCode?: string;
  divipolaCode?: string;
  validationErrors?: string[];
}

export interface IAddressValidator {
  readonly validatorName: string;
  supportsCountry(countryCode: string): boolean;
  validateAndNormalize(input: RawAddressInput): Promise<NormalizedAddress>;
}

export class UniversalAddressValidator implements IAddressValidator {
  readonly validatorName = "universal-postal";

  supportsCountry(_countryCode: string): boolean {
    return true; // Fallback universal validator
  }

  async validateAndNormalize(input: RawAddressInput): Promise<NormalizedAddress> {
    const errors: string[] = [];

    if (!input.countryCode || input.countryCode.length !== 2) {
      errors.push("Country code must be a valid 2-letter ISO 3166-1 alpha-2 code.");
    }
    if (!input.city?.trim()) {
      errors.push("City name is required.");
    }
    if (!input.streetLine1?.trim()) {
      errors.push("Street address line 1 is required.");
    }

    if (errors.length > 0) {
      return {
        isValid: false,
        standardizedCountry: input.countryCode?.toUpperCase() || "",
        standardizedState: input.stateOrProvince?.trim() || "",
        standardizedCity: input.city?.trim() || "",
        standardizedStreet: input.streetLine1?.trim() || "",
        validationErrors: errors,
      };
    }

    return {
      isValid: true,
      standardizedCountry: input.countryCode.toUpperCase(),
      standardizedState: input.stateOrProvince.trim(),
      standardizedCity: input.city.trim(),
      standardizedStreet: input.streetLine1.trim() + (input.streetLine2 ? `, ${input.streetLine2.trim()}` : ""),
      postalCode: input.postalCode?.trim(),
      divipolaCode: input.divipolaCode?.trim(),
    };
  }
}

export class DaneDivipolaAddressValidator implements IAddressValidator {
  readonly validatorName = "colombia-dane-divipola";

  supportsCountry(countryCode: string): boolean {
    return countryCode.toUpperCase() === "CO";
  }

  async validateAndNormalize(input: RawAddressInput): Promise<NormalizedAddress> {
    if (!this.supportsCountry(input.countryCode)) {
      return {
        isValid: false,
        standardizedCountry: input.countryCode,
        standardizedState: input.stateOrProvince,
        standardizedCity: input.city,
        standardizedStreet: input.streetLine1,
        validationErrors: ["DaneDivipolaAddressValidator only supports country code 'CO'."],
      };
    }

    // Validate 8-digit DANE Divipola code format (department 2 digits + municipality 3 digits + populated center 3 digits)
    const divipola = input.divipolaCode?.replace(/\D/g, "");
    const errors: string[] = [];

    if (divipola && divipola.length !== 8) {
      errors.push("Colombian DANE Divipola code must be exactly 8 digits.");
    }

    return {
      isValid: errors.length === 0,
      standardizedCountry: "CO",
      standardizedState: input.stateOrProvince.toUpperCase().trim(),
      standardizedCity: input.city.toUpperCase().trim(),
      standardizedStreet: input.streetLine1.trim(),
      divipolaCode: divipola,
      validationErrors: errors.length > 0 ? errors : undefined,
    };
  }
}
