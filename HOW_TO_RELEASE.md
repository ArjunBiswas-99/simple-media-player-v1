# 🚀 How to Create v1.0.0 Release

**Simple guide for Arjun** - Follow these steps in order!

---

## ✅ Step 1: Build the Windows .exe (5 minutes)

**On your Windows PC:**

1. Open Command Prompt
2. Navigate to project:
   ```cmd
   cd C:\Users\arjun\OneDrive\Desktop\Test\simple-media-player-v1
   ```

3. Build the executable:
   ```cmd
   python build.py
   ```
   
4. **IMPORTANT: Test the .exe!**
   - Go to `dist\` folder
   - Double-click `SimpleMediaPlayer.exe`
   - Open a video and test it works
   - If it works, continue! If not, let me know.

---

## ✅ Step 2: Commit Everything (2 minutes)

**In Command Prompt or Git Bash:**

```bash
# Navigate to project (if not already there)
cd C:\Users\arjun\OneDrive\Desktop\Test\simple-media-player-v1

# Check what needs to be committed
git status

# Add all files
git add .

# Commit with message
git commit -m "Release v1.0.0 - Initial MVP"

# Push to GitHub
git push origin main
```

---

## ✅ Step 3: Create Git Tag (1 minute)

**Still in Command Prompt/Git Bash:**

```bash
# Create tag
git tag -a v1.0.0 -m "v1.0.0 - Initial Release"

# Push tag to GitHub
git push origin v1.0.0
```

---

## ✅ Step 4: Create GitHub Release Page (5 minutes)

1. **Open browser and go to:**
   ```
   https://github.com/ArjunBiswas-99/simple-media-player
   ```

2. **Click "Releases"** (right sidebar)

3. **Click "Create a new release"** (green button)

4. **Fill in the form:**

   **Choose a tag:** 
   - Click dropdown and select `v1.0.0`
   
   **Release title:** 
   ```
   v1.0.0 - Initial Release
   ```
   
   **Description:**
   - Open file: `RELEASE_NOTES_v1.0.0.md` 
   - **Copy ALL the content**
   - **Paste into description box**
   
   **Attach binary:**
   - Click "Attach binaries by dropping them here or selecting them"
   - Navigate to: `C:\Users\arjun\OneDrive\Desktop\Test\simple-media-player-v1\dist\`
   - Select `SimpleMediaPlayer.exe`
   - Wait for upload to complete
   
   **Checkboxes:**
   - ☐ Set as a pre-release - **LEAVE UNCHECKED**
   - ✅ Set as the latest release - **CHECK THIS**

5. **Click "Publish release"** (green button at bottom)

---

## ✅ Step 5: Verify (2 minutes)

1. **Go to your releases page:**
   ```
   https://github.com/ArjunBiswas-99/simple-media-player/releases
   ```

2. **Check you see:**
   - v1.0.0 with "Latest" badge
   - Your release description
   - 3 download assets:
     - SimpleMediaPlayer.exe
     - Source code (zip)
     - Source code (tar.gz)

3. **Test downloading:**
   - Click `SimpleMediaPlayer.exe` to download
   - Verify it downloads correctly

---

## 🎉 That's It!

Your v1.0.0 is now live! 

### What happens now?

**Your development workflow STAYS THE SAME:**
- Keep testing with `python -m src.main`
- Keep fixing bugs and adding features
- Keep committing to GitHub

**When to create next release (v1.1.0, v2.0.0):**
- Only when you have significant new features
- Or major bug fixes
- Then repeat these steps with new version number

---

## 🆘 If You Need Help

Just message me and I'll help! The steps are simpler than they look:
1. Build .exe (one command)
2. Git stuff (3 commands)
3. GitHub page (copy-paste + upload)

You got this! 💪
