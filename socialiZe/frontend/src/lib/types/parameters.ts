interface RecordingProperties {
    duration: number;
    adaptationDuration: number;
    fadeInDuration: number;
    recordingName: string;
    recordingDirectory: string;
    names: {
        project: string;
        experimenter: string;
        description: string;
    }
}

export { type RecordingProperties };