"""
מעלה את כל הקבצים שנמצאים בתיקיית ההורדה (downloads/) לתיקייה
ספציפית בגוגל דרייב, בעזרת Service Account.

שימוש:
    python upload_to_drive.py downloads

דורש משתני סביבה:
    DRIVE_FOLDER_ID - מזהה התיקייה בדרייב להעלאה אליה
וקובץ:
    gha-creds.json - מפתח ה-Service Account (JSON)
"""

import os
import sys
import glob

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

CREDS_FILE = "gha-creds.json"
SCOPES = ["https://www.googleapis.com/auth/drive"]


def main():
    if len(sys.argv) < 2:
        print("שימוש: python upload_to_drive.py <תיקיית מקור>")
        sys.exit(1)

    source_dir = sys.argv[1]
    folder_id = os.environ.get("DRIVE_FOLDER_ID")

    if not folder_id:
        print("שגיאה: לא הוגדר משתנה הסביבה DRIVE_FOLDER_ID")
        sys.exit(1)

    if not os.path.exists(CREDS_FILE):
        print(f"שגיאה: קובץ ההרשאות {CREDS_FILE} לא נמצא")
        sys.exit(1)

    files = [
        f for f in glob.glob(os.path.join(source_dir, "*"))
        if os.path.isfile(f)
    ]

    if not files:
        print(f"לא נמצאו קבצים בתיקייה {source_dir}")
        sys.exit(1)

    creds = service_account.Credentials.from_service_account_file(
        CREDS_FILE, scopes=SCOPES
    )
    service = build("drive", "v3", credentials=creds)

    for file_path in files:
        file_name = os.path.basename(file_path)
        print(f"מעלה את {file_name} ...")

        file_metadata = {
            "name": file_name,
            "parents": [folder_id],
        }
        media = MediaFileUpload(file_path, resumable=True)

        uploaded = service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id, webViewLink",
        ).execute()

        print(f"הועלה בהצלחה: {uploaded.get('webViewLink')}")


if __name__ == "__main__":
    main()
