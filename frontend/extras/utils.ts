import { Currency } from "@/app/types/models";

export function formatCurrency(currency: Currency, value: string | number, posPrefix: string = "+", negPrefix: string = "-"): string {
    const numericValue = Number(value)
    const positive = numericValue >= 0
    const formattedValue = Math.abs(numericValue).toFixed(2)

    const posNegPrefix: string = (positive ? posPrefix : negPrefix);
    let prefix: string = "";
    let suffix: string = "";

    switch (currency) {
        case ("EUR"):
            prefix = "€"
            break;
        case ("GBP"):
            prefix = "£"
            break;
        case ("USD"):
            prefix = "$"
            break;
        case ("AUD"):
            prefix = "$"
            suffix = " AUD"
            break;
    }

    return `${posNegPrefix}${prefix}${formattedValue}${suffix}`
}

export function skeletonWidth(index: number, min: number, max: number) {
    if (max < min) {
        throw new Error("max must be greater than or equal to min")
    }
  return min + ((index * 37) % (max - min + 1));
}