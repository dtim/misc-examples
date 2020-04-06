import os
import io
from google.oauth2 import service_account
from google.cloud import speech_v1


def recognize(filepath, language_code='en_US', model='default', cred_file=None):
    # if cred_file is not None:
    #     cred = service_account.Credentials.from_service_account_file(
    #         cred_file,
    #         scopes=["https://www.googleapis.com/auth/cloud-platform"]
    #     )
    # 
    #     client = speech_v1.SpeechClient(credentials=cred)
    # else:
    #     client = speech_v1.SpeechClient()

    if cred_file is not None:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_file

    client = speech_v1.SpeechClient()

    config = {
        "model": model,
        "language_code": language_code
    }

    with io.open(filepath, 'rb') as fd:
        content = fd.read()

    audio = {"content": content}

    response = client.recognize(config, audio)
    for result in response.results:
        alternative = result.alternatives[0]
        yield alternative.transcript


def main():
    import argparse

    supported_models = ["command_and_search", "phone_call", "video", "default"]

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--lang", type=str, default="en_US", help="audio language")
    parser.add_argument("-m", "--model", type=str,
                        choices=supported_models,
                        default="default",
                        help="transcription model")
    parser.add_argument("--cred", type=str, help="credentials file")
    parser.add_argument("audiofile", type=str, help="path to the audio file")

    args = parser.parse_args()
    if args.cred is not None:
        print("Using credentials file:", args.cred)


    print()
    for transcript in recognize(args.audiofile, args.lang, cred_file=args.cred):
        print(transcript)
    print()


if __name__ == '__main__':
    main()
