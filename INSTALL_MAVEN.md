# Maven Installation Guide for Windows

## Quick Installation Steps

### Option 1: Download and Install Maven Manually

1. **Download Maven**:
   - Go to https://maven.apache.org/download.cgi
   - Download "Binary zip archive" (e.g., apache-maven-3.9.6-bin.zip)

2. **Extract Maven**:
   - Extract to `C:\apache-maven-3.9.6` (or any folder you prefer)

3. **Set Environment Variables**:
   - Open System Properties → Advanced → Environment Variables
   - Add new System Variable:
     - Variable name: `MAVEN_HOME`
     - Variable value: `C:\apache-maven-3.9.6`
   - Edit the `Path` variable and add: `%MAVEN_HOME%\bin`

4. **Verify Installation**:
   ```cmd
   mvn --version
   ```

### Option 2: Using Chocolatey (if installed)

```cmd
choco install maven
```

### Option 3: Using Scoop (if installed)

```cmd
scoop install maven
```

## After Maven Installation

1. **Restart your command prompt**
2. **Navigate to project directory**:
   ```cmd
   cd C:\project\id
   ```
3. **Run the build script**:
   ```cmd
   build_and_run.bat
   ```

## Alternative: Use IDE with Built-in Maven

If you prefer not to install Maven separately:

1. **IntelliJ IDEA Community** (Free):
   - Download from https://www.jetbrains.com/idea/download/
   - Open the project folder
   - IntelliJ will automatically detect the Maven project
   - Click "Run" to start the application

2. **Eclipse IDE** (Free):
   - Download from https://www.eclipse.org/downloads/
   - Import as "Existing Maven Project"
   - Right-click project → Run As → Spring Boot App

3. **Visual Studio Code** (Free):
   - Install "Extension Pack for Java"
   - Open project folder
   - Use integrated terminal to run Maven commands

## Quick Test

After installation, test with:
```cmd
mvn --version
java -version
```

Both should show version information.

## Next Steps

Once Maven is installed:
1. Run `build_and_run.bat` to build and start the Java application
2. Test the API endpoints using `python test_java_api.py`
3. Access the system at http://localhost:8080