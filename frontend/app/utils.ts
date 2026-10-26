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

export function deCapitalise(text: string): string {
    let out = []

    for (let i = 0; i < text.length; i++) {
        const char: string = text[i];

        if (i === 0 || (text[i - 1] && text[i - 1] === " ")) {
            // capitalise if start of string or after space
            out.push(char)

        } else {
            out.push(char.toLowerCase())
        }
    }
    return out.join("");
}

export function formatTransactionDescription(text: string): string {
    let out = []

    for (let i = 0; i < text.length; i++) {
        const char: string = text[i];

        console.log(text.slice(i, i + 4).toLowerCase())

        if (text.slice(i, i + 4).toLowerCase() === "www.") {
            // make 'www.' lowercase
            out.push(char.toLowerCase())
        } else if (i === 0 || text[i - 1] === " ") {
            // capitalise if start of string or after space
            out.push(char)
        } else {
            out.push(char.toLowerCase())
        }
    }

    return out.join("")
}

export function formatTransactionDate(date: string): string {
    const parsedDate = new Date(date);

    const day = parsedDate.getDate();

    const month = parsedDate.toLocaleDateString("en-GB", {
        month: "short",
    });

    const year = parsedDate.getFullYear();

    return `${day} ${month}, ${year}`;
}

export function formatLongTransactionDate(date: string): string {
    const parsedDate = new Date(date);

    const day = parsedDate.getDate();

    const weekday = parsedDate.toLocaleDateString("en-GB", {
        weekday: "long"
    })

    const month = parsedDate.toLocaleDateString("en-GB", {
        month: "long",
    });

    const year = parsedDate.getFullYear();

    return `${weekday} ${day} ${month}, ${year}`;
}

export function formatTransactionCategory(text: string): string {
    return (deCapitalise(text.replace("_", " ")))
}