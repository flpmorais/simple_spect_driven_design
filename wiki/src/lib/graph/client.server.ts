import { execFile } from 'node:child_process';
import { access } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { promisify } from 'node:util';

const execFileAsync = promisify(execFile);

export class GraphReadError extends Error {
	code: string;

	constructor(message: string, code = 'graph_read_error') {
		super(message);
		this.name = 'GraphReadError';
		this.code = code;
	}
}

async function findRepoRoot(start: string): Promise<string> {
	let current = start;

	while (true) {
		const scriptPath = join(current, '.opencode/scripts/ssd_memory/memory.py');
		try {
			await access(scriptPath);
			return current;
		} catch {
			const parent = dirname(current);
			if (parent === current) {
				throw new GraphReadError('Could not locate SSD memory script', 'memory_script_missing');
			}
			current = parent;
		}
	}
}

async function runScriptCommand<T>(scriptRelativePath: string, args: string[]): Promise<T> {
	const repoRoot = await findRepoRoot(process.cwd());
	const scriptPath = join(repoRoot, scriptRelativePath);

	try {
		const { stdout } = await execFileAsync('python3', [scriptPath, ...args], {
			cwd: repoRoot,
			maxBuffer: 1024 * 1024 * 10
		});
		return JSON.parse(stdout) as T;
	} catch (error) {
		if (error instanceof SyntaxError) {
			throw new GraphReadError('Memory command returned invalid JSON', 'invalid_memory_json');
		}

		if (typeof error === 'object' && error !== null && 'stderr' in error) {
			throw parseError(String(error.stderr ?? ''));
		}

		throw new GraphReadError(error instanceof Error ? error.message : 'Memory command failed');
	}
}

function parseError(stderr: string): GraphReadError {
	const text = stderr.trim();
	if (!text) return new GraphReadError('Memory command failed');

	try {
		const parsed = JSON.parse(text) as { error?: unknown; status?: unknown };
		if (typeof parsed.error === 'string') {
			return new GraphReadError(parsed.error, typeof parsed.status === 'string' ? parsed.status : undefined);
		}
	} catch {
		// Fall through to raw stderr text.
	}

	return new GraphReadError(text);
}

export async function runMemoryCommand<T>(args: string[]): Promise<T> {
	return runScriptCommand('.opencode/scripts/ssd_memory/memory.py', args);
}

export async function runBrainstormCommand<T>(args: string[]): Promise<T> {
	return runScriptCommand('.opencode/scripts/ssd_brainstorming/memory.py', args);
}
