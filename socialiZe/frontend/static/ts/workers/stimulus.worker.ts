import { createPath } from '../helpers/predefinedPaths.js';

const connectedPorts: ConnectedPort[] = [];

// Store the uploaded coordinates from the file
let uploadedCoordinates: { x: number, y: number, coords: number }[] = [];


let stimulusProperties: StimulusProperties = {
    dotProperties: {
        colour: 'black',
        size: 10,
        opacity: 1
    },
    jumpFactor: 10,
    speed: 30,
    coordinates: []
};

let recordingProperties: RecordingProperties = {
    duration: 0,
    adaptationDuration: 0,
    fadeInDuration: 0,
    recordingName: '',
    recordingDirectory: '',
    names: {
        project: '',
        experimenter: '',
        description: ''
    }
};

interface SetDotPathEvent {
    type: 'SET_DOT_PATH';
    data: SetDotPathData;
}

interface SetDotPathData {
    pathType: 'predefined' | 'file';
    pathData: PathData | FilePathData;
    resend?: boolean;
}

interface PathData {
    type: string;
    speed: number;
    jumpFactor: number;
}

interface FilePathData {
    speed?: number;
    jumpFactor?: number;
    fileData: {
        name: string;
        size: string;
        lines: number;
    },
    pathCoordinates: { x: number, y: number, coords: number }[];
}

interface DotPathEvent {
    type: 'DOT_PATH';
    data: {
        pathType: 'predefined' | 'file';
        pathCoordinates: { x: number, y: number, coords: number }[];
        pathData: PathData | FilePathData;
    }
}

interface StimulusProperties {
    dotProperties: DotProperties;
    jumpFactor: number;
    speed: number;
    coordinates: { x: number, y: number, coords: number }[];
}

interface DotProperties {
    colour: string;
    size: number;
    opacity: number;
}

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

interface RecordingPropertiesEvent {
    type: 'RECORDING_PROPERTIES';
    data: RecordingProperties;
}

interface ResetEvent {
    type: 'RESET';
}

interface ReadyEvent {
    type: 'READY';
}

interface ConnectedPort {
    port: MessagePort;
    isReady: boolean;
}

type WorkerEvent = SetDotPathEvent | DotPathEvent | ResetEvent | ReadyEvent;


function setDotPathHandler(data: SetDotPathData) {
    const { pathType, pathData, resend } = data;

    // Log the path being changed
    console.log(`Setting the path to ${pathType} path.`);

    // Create the path based on the path type
    let path: { x: number, y: number, coords: number }[] = [];
    let dotPathEvent: DotPathEvent;
    if (pathType === 'predefined') {
        const pathDataTyped = pathData as PathData;
        const speed = pathDataTyped.speed;
        const jumpFactor = pathDataTyped.jumpFactor;
        path = createPath(pathDataTyped.type, 1000, jumpFactor);

        // Set the dot properties
        stimulusProperties = {
            ...stimulusProperties,
            jumpFactor: jumpFactor,
            speed: speed,
            coordinates: path
        };

        dotPathEvent = { type: 'DOT_PATH', data: {
            pathType: 'predefined',
            pathCoordinates: path,
            pathData: {
                type: pathDataTyped.type,
                speed: pathDataTyped.speed,
                jumpFactor: pathDataTyped.jumpFactor
            }
        } };
    } else if (pathType === 'file') {
        const pathDataTyped = pathData as FilePathData;
        const jumpFactor = pathDataTyped.jumpFactor;
        const speed = pathDataTyped.speed;

        if (resend === true) {
            path = uploadedCoordinates;
        } else {
            path = pathDataTyped.pathCoordinates;
        }

        path = path.filter((coordinate) => {
            return coordinate.x !== 0 && coordinate.y !== 0;
        });

        // Set the dot properties
        stimulusProperties = {
            ...stimulusProperties,
            jumpFactor: jumpFactor || 10,
            speed: speed || 30,
            coordinates: path
        };

        uploadedCoordinates = path;
        dotPathEvent = { type: 'DOT_PATH', data: {
            pathType: 'file',
            pathCoordinates: path,
            pathData: {
                type: 'file',
                speed: speed || 30,
                jumpFactor: jumpFactor || 10
            }
        } };
    }

    connectedPorts.forEach((connectedPort) => {
        if (connectedPort.isReady) {
            connectedPort.port.postMessage(dotPathEvent);
        }
    });
}

function setDotPropertiesHandler(data: DotProperties) {
    stimulusProperties = {
        ...stimulusProperties,
        dotProperties: data
    };

    connectedPorts.forEach((connectedPort) => {
        if (connectedPort.isReady) {
            connectedPort.port.postMessage({ type: 'SET_DOT_PROPERTIES', data: {
                colour: data.colour,
                size: data.size,
                opacity: data.opacity
            } });
        }
    });
}

function setRecordingPropertiesHandler(data: RecordingProperties) {
    recordingProperties = data;

    // Create the file name and directory
    const date = new Date();
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();

    // Create the recording name
    const dateString: string = `${year}-${month}-${day}`;
    const projectString: string = recordingProperties.names.project.replace(/ /g, '-');
    const experimenterString: string = recordingProperties.names.experimenter.replace(/ /g, '-');
    const descriptionString: string = recordingProperties.names.description.replace(/ /g, '-');
    const recordingName: string = `${dateString}_${projectString}_${experimenterString}_${descriptionString}`;

    // Create the recording directory
    const recordingDirectory: string = `~/Documents/socialiZe/${experimenterString}/recordings`;

    // Set the recording properties
    recordingProperties = {
        ...recordingProperties,
        recordingName,
        recordingDirectory
    };

    connectedPorts.forEach((connectedPort) => {
        if (connectedPort.isReady) {
            connectedPort.port.postMessage({ type: 'RECORDING_PROPERTIES', data: recordingProperties });
        }
    });
}

function setRestartAnimationHandler() {
    connectedPorts.forEach((connectedPort) => {
        connectedPort.port.postMessage({ type: 'RESET' });
    });

    // Send each port the data via the 'DOT_PATH' event
    connectedPorts.forEach((connectedPort) => {
        connectedPort.port.postMessage({ type: 'DOT_PATH', data: {
            // pathType: 'predefined',
            pathData: {
                pathCoordinates: stimulusProperties.coordinates,
                speed: stimulusProperties.speed,
                jumpFactor: stimulusProperties.jumpFactor
            }
        } });
    });
}


self.addEventListener('connect', (event) => {
    const port = (event as MessageEvent).ports[0];
    connectedPorts.push({ port, isReady: false });

    port.addEventListener('message', (event) => {
        const { type, data } = event.data;

        if (type === 'SET_DOT_PATH') {
            setDotPathHandler(data);
        } else if (type === 'SET_DOT_PROPERTIES') {
            // connectedPorts.forEach((connectedPort) => {
            //     connectedPort.port.postMessage({ type: 'SET_DOT_PROPERTIES', data });
            // });
            setDotPropertiesHandler(data);
        } else if (type === 'SET_RECORDING_PROPERTIES') {
            setRecordingPropertiesHandler(data);
        } else if (type === 'START_TRIAL') {
            connectedPorts.forEach((connectedPort) => {
                connectedPort.port.postMessage({ type: 'START_TRIAL', data: recordingProperties });
            });

            // Send the first coordinate to the port
            const connectedPort = connectedPorts.find((cp) => cp.port === port);
            if (connectedPort) {

                // Send the first non-zero coordinate
                const firstNonZeroCoordinate = stimulusProperties.coordinates.find((coordinate) => {
                    return coordinate.x !== 0 && coordinate.y !== 0;
                });
                
                connectedPort.port.postMessage({ type: 'FIRST_COORDINATE', data: {
                    coordinate: stimulusProperties.coordinates[0]
                }});
            }

            // Send a request to the backend to start the recording

        } else if (type === 'RESET') {
            console.log('Resetting the path');

            // Reset the path
            connectedPorts.forEach((connectedPort) => {
                connectedPort.port.postMessage({ type: 'RESET' });
            });
        } else if (type === 'READY') {
            const connectedPort = connectedPorts.find((cp) => cp.port === port);
            if (connectedPort) {
                connectedPort.isReady = true;
            }
        } else if (type === 'READY_POPOUT') {
            const connectedPort = connectedPorts.find((cp) => cp.port === port);
            if (connectedPort) {
                connectedPort.isReady = true;
                connectedPort.port.postMessage({ type: 'POPOUT_PROPERTIES', data: {
                    recordingProperties: recordingProperties,
                    stimulusProperties: stimulusProperties
                }});
            }
        } else if (type === 'RESTART_ANIMATION') {
            connectedPorts.forEach((connectedPort) => {
                connectedPort.port.postMessage({ type: 'RESTART_ANIMATION' });
            });
        } else if (type === 'STOP_ANIMATION') {
            connectedPorts.forEach((connectedPort) => {
                connectedPort.port.postMessage({ type: 'STOP_ANIMATION' });
            });
        }
    });

    port.start();
});

export {};