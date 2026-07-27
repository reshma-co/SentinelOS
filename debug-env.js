// ...existing code...
const fs = require('fs');
const path = require('path');

const envPath = path.join(__dirname, '.env');
console.log('Debugging env for NitroStack');
console.log('Repo path:', __dirname);

let fileContent = '';
try {
    fileContent = fs.readFileSync(envPath, 'utf8');
} catch (err) {
    console.error('.env file not found at', envPath);
    process.exit(2);
}

function parseDotEnv(content) {
    const lines = content.split(/\r?\n/);
    const result = {};
    for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed || trimmed.startsWith('#') || trimmed.startsWith(';')) continue;
        const eq = trimmed.indexOf('=');
        if (eq === -1) continue;
        const key = trimmed.slice(0, eq).trim();
        let val = trimmed.slice(eq + 1).trim();
        if (val.startsWith('"') && val.endsWith('"')) val = val.slice(1, -1);
        if (val.startsWith("'") && val.endsWith("'")) val = val.slice(1, -1);
        result[key] = val;
    }
    return result;
}

const parsed = parseDotEnv(fileContent);
const keys = [
    'OPENWEATHER_API_KEY',
    'OPENAI_API_KEY',
    'ANTHROPIC_API_KEY',
    'GITHUB_TOKEN',
    'API_HOST',
    'API_PORT'
];

console.log('\nVariables found in .env file:');
keys.forEach(k => console.log(k + ':', (k in parsed) ? '[IN_FILE]' : '[NOT_IN_FILE]'));

console.log('\nVariables available to Node process (process.env):');
keys.forEach(k => console.log(k + ':', process.env[k] ? '[SET]' : '[MISSING]'));

console.log('\nDetailed values from .env (masked):');
for (const k of Object.keys(parsed)) {
    const v = parsed[k];
    const masked = v && v.length > 6 ? v.slice(0, 3) + '...' + v.slice(-3) : (v ? '***' : '(empty)');
    console.log(k + ':', masked);
}

console.log('\nIf values are present in the .env file but missing in process.env, ensure your application loads the .env (e.g., require("dotenv").config()) at startup or set the variables in your deployment environment.');
