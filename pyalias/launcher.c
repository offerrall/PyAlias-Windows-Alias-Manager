#include <windows.h>
#include <stdio.h>
#include <string.h>

#define MAX_PATH_EXTENDED 32768
#define MAX_NAME 256
#define MAX_COMMAND 8192

int get_program_name(char *output, size_t output_size) {
    char fullPath[MAX_PATH_EXTENDED];
    
    DWORD result = GetModuleFileNameA(NULL, fullPath, MAX_PATH_EXTENDED);
    
    if (result == 0) {
        printf("ERROR: GetModuleFileName failed\n");
        return 0;
    }
    
    if (result >= MAX_PATH_EXTENDED) {
        printf("ERROR: Path too long\n");
        return 0;
    }
    
    char *lastSlash = strrchr(fullPath, '\\');
    char *fileName = (lastSlash == NULL) ? fullPath : lastSlash + 1;
    
    size_t nameLen = strlen(fileName);
    
    if (nameLen < 5) {
        printf("ERROR: Filename too short\n");
        return 0;
    }
    
    if (nameLen >= output_size) {
        printf("ERROR: Filename too long for buffer\n");
        return 0;
    }
    
    if (strcmp(fileName + nameLen - 4, ".exe") != 0) {
        printf("ERROR: File does not end in .exe\n");
        return 0;
    }
    
    size_t copyLen = nameLen - 4;
    if (copyLen >= output_size) {
        printf("ERROR: Name too long for output buffer\n");
        return 0;
    }
    
    strncpy(output, fileName, copyLen);
    output[copyLen] = '\0';
    
    return 1;
}

int get_program_directory(char *output, size_t output_size) {
    char fullPath[MAX_PATH_EXTENDED];
    
    DWORD result = GetModuleFileNameA(NULL, fullPath, MAX_PATH_EXTENDED);
    
    if (result == 0) {
        printf("ERROR: GetModuleFileName failed\n");
        return 0;
    }
    
    if (result >= MAX_PATH_EXTENDED) {
        printf("ERROR: Path too long\n");
        return 0;
    }
    
    char *lastSlash = strrchr(fullPath, '\\');
    
    if (lastSlash == NULL) {
        printf("ERROR: No backslash found in path\n");
        return 0;
    }
    
    size_t dirLen = lastSlash - fullPath + 1;
    
    if (dirLen >= output_size) {
        printf("ERROR: Directory path too long for buffer\n");
        return 0;
    }
    
    strncpy(output, fullPath, dirLen);
    output[dirLen] = '\0';
    
    return 1;
}

int get_txt_filepath(const char *programName, const char *programDir, char *output, size_t output_size) {
    size_t nameLen = strlen(programName);
    size_t dirLen = strlen(programDir);
    size_t totalLen = dirLen + nameLen + 4 + 1;
    
    if (totalLen > output_size) {
        printf("ERROR: Combined path too long for buffer\n");
        return 0;
    }
    
    strcpy(output, programDir);
    strcat(output, programName);
    strcat(output, ".txt");
    
    return 1;
}

int read_txt_file(const char *filepath, char *output, size_t output_size) {
    FILE *fp = fopen(filepath, "r");
    
    if (fp == NULL) {
        printf("ERROR: Could not open file: %s\n", filepath);
        return 0;
    }
    
    fseek(fp, 0, SEEK_END);
    long fileSize = ftell(fp);
    rewind(fp);
    
    if (fileSize < 0) {
        printf("ERROR: Could not get file size\n");
        fclose(fp);
        return 0;
    }
    
    if ((size_t)fileSize >= output_size) {
        printf("ERROR: File too large for buffer\n");
        fclose(fp);
        return 0;
    }
    
    size_t bytesRead = fread(output, 1, fileSize, fp);
    
    if (bytesRead != (size_t)fileSize) {
        printf("ERROR: Could not read complete file\n");
        fclose(fp);
        return 0;
    }
    
    output[bytesRead] = '\0';
    fclose(fp);
    
    return 1;
}

int append_arguments(const char *baseCommand, int argc, char *argv[], char *output, size_t output_size) {
    size_t currentLen = strlen(baseCommand);
    
    if (currentLen >= output_size) {
        printf("ERROR: Base command too long\n");
        return 0;
    }
    
    strcpy(output, baseCommand);
    
    for (int i = 1; i < argc; i++) {
        size_t argLen = strlen(argv[i]);
        
        if (currentLen + 1 + argLen >= output_size) {
            printf("ERROR: Command with arguments too long\n");
            return 0;
        }
        
        strcat(output, " ");
        strcat(output, argv[i]);
        currentLen += 1 + argLen;
    }
    
    return 1;
}

int main(int argc, char *argv[]) {
    char programName[MAX_NAME];
    char programDir[MAX_PATH_EXTENDED];
    char txtFilePath[MAX_PATH_EXTENDED];
    char baseCommand[MAX_COMMAND];
    char fullCommand[MAX_COMMAND];
    
    if (!get_program_name(programName, MAX_NAME)) {
        return 1;
    }
    
    if (!get_program_directory(programDir, MAX_PATH_EXTENDED)) {
        return 1;
    }
    
    if (!get_txt_filepath(programName, programDir, txtFilePath, MAX_PATH_EXTENDED)) {
        return 1;
    }
    
    if (!read_txt_file(txtFilePath, baseCommand, MAX_COMMAND)) {
        return 1;
    }
    
    if (!append_arguments(baseCommand, argc, argv, fullCommand, MAX_COMMAND)) {
        return 1;
    }
    
    system(fullCommand);
    
    return 0;
}