שירות הורדת יוטיוב: Google Forms → Apps Script → GitHub Actions → Google Drive
מבנה הפרויקט
```
.github/workflows/download.yml   # ה-workflow שמוריד ומעלה
upload_to_drive.py               # סקריפט ההעלאה לדרייב
AppsScript.gs                    # קוד להדבקה בעורך Apps Script
```
שלבי הקמה
1. Service Account בגוגל
Google Cloud Console → פרויקט חדש
APIs & Services → Library → חיפוש "Google Drive API" → Enable
APIs & Services → Credentials → Create Credentials → Service Account
בתוך ה-Service Account: Keys → Add Key → JSON → הורדה
שתפו את תיקיית הדרייב הרצויה עם כתובת המייל של ה-Service Account
(נראית כמו `xxx@yyy.iam.gserviceaccount.com`), עם הרשאת עריכה
2. הריפו בגיטהאב
העלו את שלושת הקבצים (חוץ מ-`AppsScript.gs`) לריפו פרטי
Settings → Secrets and variables → Actions → New repository secret:
`GCP_SA_KEY` — כל תוכן קובץ ה-JSON שהורדתם
`DRIVE_FOLDER_ID` — ה-ID מתוך כתובת ה-URL של התיקייה בדרייב
(החלק אחרי `/folders/`)
3. Personal Access Token
GitHub → Settings → Developer settings → Personal access tokens →
Fine-grained tokens → Generate new token
הרשאה: Repository permissions → Actions → Read and write, על
הריפו הספציפי
שמרו את ה-token - הוא יוצג פעם אחת בלבד
4. Apps Script
פתחו את עורך הסקריפטים מתוך הטופס (⋮ → Script editor) או מתוך
גיליון התשובות (Extensions → Apps Script)
הדביקו את תוכן `AppsScript.gs`
Project Settings → Script Properties → הוסיפו:
`GITHUB_TOKEN` = ה-token מהשלב הקודם
`GITHUB_OWNER` = שם המשתמש/הארגון בגיטהאב
`GITHUB_REPO` = שם הריפו
ב-`onFormSubmit`, ודאו שהשם `'קישור ליוטיוב'` תואם בדיוק לשם
השאלה בטופס שלכם
Triggers (שעון מצד שמאל) → Add Trigger → Function: `onFormSubmit`
→ Event source: From form → Event type: On form submit
5. בדיקה
הריצו ידנית את `testTrigger` מתוך עורך Apps Script כדי לוודא שהחיבור
לגיטהאב תקין, בלי למלא טופס בפועל
עקבו אחרי הריצה בטאב Actions בריפו
בסיום, הקובץ אמור להופיע בתיקיית הדרייב שהוגדרה
פתרון בעיות נפוצות
בעיה	סיבה אפשרית
`403` בהעלאה לדרייב	התיקייה לא שותפה עם ה-Service Account
`Sign in to confirm you're not a bot`	נסו client אחר: `--extractor-args "youtube:player_client=ios"`
ה-workflow לא מופעל כלל	בדקו ש-`GITHUB_TOKEN` תקין ושה-`ref` ב-Apps Script תואם לשם הברנץ' (`main`/`master`)
הסרטון ארוך מדי / timeout	הגדילו את `timeout-minutes` ב-workflow, או הורידו באיכות נמוכה יותר
