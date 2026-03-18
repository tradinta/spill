import express from 'express';
import cors from 'cors';
import { exec } from 'child_process';
import path from 'path';
import fs from 'fs/promises';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(cors());
app.use(express.json());

const toolsDir = path.join(__dirname, '..');

const getJsonFilename = (engine, target) => {
    // Sanitize target for filename
    const safeTarget = target.replace(/[^a-zA-Z0-9_\-]/g, '');
    switch(engine) {
        case 'x': return `dossier_x_${safeTarget}.json`;
        case 'reddit': return `dossier_reddit_${safeTarget}.json`;
        case 'tiktok': return `dossier_${safeTarget}.json`;
        case 'instagram': return `dossier_instagram_${safeTarget}.json`;
        case 'linkedin': return `dossier_linkedin_${safeTarget}.json`;
        case 'facebook': return `dossier_facebook_${safeTarget}.json`;
        default: return null;
    }
}

const getScriptName = (engine) => {
    switch(engine) {
        case 'x': return 'x_intel.py';
        case 'reddit': return 'reddit_intel.py';
        case 'tiktok': return 'tiktok_intel.py';
        case 'instagram': return 'instagram_intel.py';
        case 'linkedin': return 'linkedin_intel.py';
        case 'facebook': return 'facebook_intel.py';
        default: return null;
    }
}

app.post('/api/extract', async (req, res) => {
    const { engine, target } = req.body;
    
    if (!engine || !target) {
        return res.status(400).json({ error: 'Missing engine or target' });
    }

    const scriptName = getScriptName(engine);
    
    // Clean target for the CLI
    let rawTarget = target.trim();
    rawTarget = rawTarget.replace(/^@/, '');
    if (engine === 'reddit') rawTarget = rawTarget.replace(/^u\//, '');
    if (engine === 'facebook') rawTarget = rawTarget.replace(/^profile\.php\?id=/, '');

    const jsonFilename = getJsonFilename(engine, rawTarget);
    
    if (!scriptName || !jsonFilename) {
        return res.status(400).json({ error: 'Invalid engine' });
    }
    
    const cmd = `python ${scriptName} ${rawTarget}`;
    console.log(`[API] Executing: ${cmd}`);

    // Increased timeout for long-running scrapers
    exec(cmd, { cwd: toolsDir, timeout: 90000 }, async (error, stdout, stderr) => {
        try {
            const jsonPath = path.join(toolsDir, jsonFilename);
            console.log(`[API] Attempting to read: ${jsonPath}`);
            const data = await fs.readFile(jsonPath, 'utf8');
            const parsed = JSON.parse(data);
            res.json(parsed);
        } catch (readError) {
            console.error('[API] Failed to read resulting JSON:', readError);
            res.status(500).json({ 
                error: 'Failed to generate or read intelligence dossier.', 
                details: error ? error.message : readError.message 
            });
        }
    });
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`OSINT API Server running on port ${PORT} - Backend actively bridged to Python tools.`);
});
