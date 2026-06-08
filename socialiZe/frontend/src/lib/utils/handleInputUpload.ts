import { dotProperties } from "$lib/stores/dotTestStore";
import Papa from "papaparse";
import type { Writable } from "svelte/store";


/**
 * Handles the upload of a file.
 * 
 * @param file - The file to be uploaded, either as a string or a Blob.
 * @returns A Promise that resolves to an object containing the filename, filesize, and number of lines in the uploaded file.
 */
export const handleFileUpload = async (file: string | Blob): Promise<{
    filename: string;
    filesize: number;
    numLines: number;
}> => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://localhost:8000/api/upload", {
        method: "POST",
        body: formData,
    });

    if (response.ok) {
        console.log("File uploaded successfully");

        // Use the response to get the file path.
        const r = await response.json();

        // Get the file path
        const filepath = `http://localhost:8000${r.filepath}`;

        // Get the raw name
        const rawName = r.raw_filename;

        // Get the file size
        const filesize = r.filesize;

        // Get the number of lines in the CSV file.
        const numLines = r.num_lines;

        // Set dotProperties.test.file to the raw filename.
        dotProperties.update((n) => {
            n.test.filename = rawName;
            return n;
        });

        return {
            filename: rawName,
            filesize: filesize,
            numLines: numLines,
        }
    } else {
        console.error("File upload failed");
    }

    return {
        filename: "",
        filesize: 0,
        numLines: 0,
    };

};


/**
 * Resets the file upload.
 */
export const resetFileUpload = (): void => {
    // Reset dotProperties.test.file to its initial state.
    dotProperties.update((n) => {
        n.test.filename = "";
        return n;
    });
};
