import { fallbackUserProfile } from "./constants";
import { HasProfilePic, GetProfilePic } from "./wailsjs/go/app/App";;

export const ChangeImgElSrcToFileData = async (imageEl: HTMLImageElement, file: File): Promise<void> => {
    const dataUrl = await ImgFileToDataURL(file);
    imageEl.src = dataUrl;
};

export const Base64ImgStringToFile = (base64EncodedImageString: string, fileName: string, imageType: string): File => {
    const mimetype = `image/${imageType}`;
    const binaryData = Uint8Array.from(atob(base64EncodedImageString), c => c.charCodeAt(0)); // decode base64 string
    const file = new File([binaryData], fileName, { type: mimetype });
    return file;
};

// opposite of Uint8Array.from(atob(base64EncodedImageString), c => c.charCodeAt(0)); // decode base64 string
export const GetBase64ImgStringFromFile = async (file: File): Promise<string> => {
    const data = await file.arrayBuffer();
    const base64String = btoa(new Uint8Array(data).reduce((data, byte) => data + String.fromCharCode(byte), ''));
    return base64String;
}

export const ImgFileToDataURL = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e: ProgressEvent<FileReader>): void => {
            const target = e.target as FileReader;
            const result = target.result as string;
            resolve(result);
        };
        reader.readAsDataURL(file);
    });
}

export const fallbackUserProfileFile = Base64ImgStringToFile(fallbackUserProfile, "user-profile.png", "png");

let fallbackUserProfileDataUrl: string | null = null;
export const GetFallbackUserProfileDataUrl = async (): Promise<string> => {
    if (fallbackUserProfileDataUrl !== null) {
        return fallbackUserProfileDataUrl;
    }

    fallbackUserProfileDataUrl = await ImgFileToDataURL(fallbackUserProfileFile);
    return fallbackUserProfileDataUrl;
};

export const GetProfilePicURL = async (hasProfilePic: boolean | null = null): Promise<string> => {
    if ((hasProfilePic !== null && !hasProfilePic) || !(await HasProfilePic())) {
        return await GetFallbackUserProfileDataUrl();
    }

    const { Data, Type } = await GetProfilePic();;
    const mimetype = `image/${Type}`;

    const file = Base64ImgStringToFile(Data, "profile-pic.png", mimetype);
    const uploadedProfilePicURL = await ImgFileToDataURL(file);
    return uploadedProfilePicURL;
};
