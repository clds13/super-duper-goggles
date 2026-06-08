export let worker: SharedWorker | undefined;
let x = 1;

if (typeof window !== 'undefined') {
    worker = new SharedWorker('/js/workers/stimulus.worker.js', { type: 'module' });
}