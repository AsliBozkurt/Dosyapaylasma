import { createI18n } from 'vue-i18n'


const numberFormats = {
    'en-gb': {
        currency: {
            style: 'currency',
            currency: 'USD',
            notation: 'standard'
        },
        decimal: {
            style: 'decimal',
            minimumFractionDigits: 0,
            maximumFractionDigits: 2
        },
        percent: {
            style: 'percent',
            useGrouping: false
        }
    },
    'tr': {
        currency: {
            style: 'currency',
            currency: 'TRL',
            useGrouping: true,
            currencyDisplay: 'symbol'
        },
        decimal: {
            style: 'decimal',
            minimumFractionDigits: 0,
            maximumFractionDigits: 2
        },
        percent: {
            style: 'percent',
            useGrouping: false
        }
    }
}

const datetimeFormats = {
    'en-gb': {
        short: {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        },
        long: {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            weekday: 'short',
            hour: 'numeric',
            minute: 'numeric',
            hour12: true
        }
    },
    'tr': {
        short: {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        },
        long: {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            weekday: 'short',
            hour: 'numeric',
            minute: 'numeric',
            hour12: false
        }
    }
}


// const dateTimeFormats = {
//     'en-gb': {
//         short: {
//             year: 'numeric',
//             month: 'short',
//             day: 'numeric'
//         },
//         middle: {
//             year: 'numeric',
//             month: 'short',
//             day: 'numeric',
//             hour: 'numeric',
//             minute: 'numeric',
//             hour12: true
//         },
//         long: {
//             year: 'numeric',
//             month: 'long',
//             day: 'numeric',
//             weekday: 'long',
//             hour: 'numeric',
//             minute: 'numeric',
//             hour12: true
//         }
//     },
//     'tr': {
//         short: {
//             year: 'numeric',
//             month: 'short',
//             day: 'numeric'
//         },
//         middle: {
//             year: 'numeric',
//             month: 'short',
//             day: 'numeric',
//             hour: 'numeric',
//             minute: 'numeric',
//             hour12: false
//         },
//         long: {
//             year: 'numeric',
//             month: 'long',
//             day: 'numeric',
//             weekday: 'long',
//             hour: 'numeric',
//             minute: 'numeric',
//             hour12: false
//         }
//     }
// }

function loadLocaleMessages() {
    const locales = require.context('./locales', true, /[A-Za-z0-9-_,\s]+\.json$/i)
    const messages = {}
    locales.keys().forEach(key => {
        const matched = key.match(/([A-Za-z0-9-_]+)\./i)
        if (matched && matched.length > 1) {
            const locale = matched[1]
            messages[locale] = locales(key)
        }
    })
    return messages
}

export function GetLangJs() {
    const i18n = createI18n({
        locale: 'en-GB' || 'en-GB',
        fallbackLocale: 'en-GB' || 'en-GB',
        numberFormats,
        datetimeFormats,
        messages: loadLocaleMessages()

    })
    return i18n
}