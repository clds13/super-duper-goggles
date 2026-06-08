import fs from 'fs';
import readline from 'readline';

/**
 * Asynchronously reads a range of lines from a CSV file.
 * 
 * @param {string} filePath - The path to the CSV file.
 * @param {number} startLine - The starting line number (inclusive).
 * @param {number} endLine - The ending line number (inclusive).
 * @returns {Promise<string[]>} - A promise that resolves with an array of lines.
 */
async function readCSVFromDLC(filePath: string, startLine: number, endLine: number): Promise<string[]> {
    return new Promise((resolve, reject) => {
        const lines: string[] = [];
        let currentLine = 0;

        const stream = fs.createReadStream(filePath);
        const lineReader = readline.createInterface({
            input: stream,
            crlfDelay: Infinity,
        });

        lineReader.on('line', (line) => {
            currentLine++;
            if (currentLine >= startLine && currentLine <= endLine) {
                lines.push(line);
            }
            if (currentLine > endLine) {
                lineReader.close();
            }
        });

        lineReader.on('close', () => {
            resolve(lines);
        });

        lineReader.on('error', (err) => {
            reject(err);
        });
    });
}

/**
 * Parses a range of lines from a CSV file and returns a map of row numbers to an array of values.
 * @param filename - The path to the CSV file.
 * @param startLine - The starting line number (inclusive).
 * @param endLine - The ending line number (inclusive).
 * @returns A map of row numbers to an array of values.
 */
export async function parseCSVFromDLC(filename: string, startLine: number, endLine: number): Promise<object> {
    const lines = await readCSVFromDLC(filename, startLine, endLine);
    const csvValues: Map<string, string[]> = new Map();

    for (let i = 0; i < lines.length; i++) {
        const values = lines[i].split(',');
        csvValues.set(`row${i + 1}`, values);
    }

    return csvValues;
}
