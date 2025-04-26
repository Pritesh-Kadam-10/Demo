pipeline {
    agent any

    environment {
        TARGET_BRANCH = "main"
        SOURCE_BRANCH = "pritesh/test/jenkins"
        REPO_URL = 'https://github.com/Pritesh-Kadam-10/Demo.git'
    }

    stages {
        stage('Clone Repository') {
            steps {
                sh 'rm -rf workspace_old workspace_new'
                sh 'mkdir workspace_old workspace_new'
                
                echo '📦 Cloning main branch (OLD files)...'
                dir('workspace_old') {
                    git branch: "${TARGET_BRANCH}", url: "${REPO_URL}"
                }

                echo '📦 Cloning PR branch (NEW files)...'
                dir('workspace_new') {
                    git branch: "${SOURCE_BRANCH}", url: "${REPO_URL}"
                }
            }
        }

        stage('Prepare Changed Files') {
            steps {
                sh '''
                echo '🛠 Identifying changed files...'
                
                cd workspace_new
                git fetch origin ${TARGET_BRANCH}
                git diff --name-only origin/${TARGET_BRANCH}..origin/${SOURCE_BRANCH} > ../changed_files.txt || true
                cd ..

                mkdir -p output/old_files
                mkdir -p output/new_files

                echo '📋 Copying only changed files...'
                while IFS= read -r file; do
                  if [ -f "workspace_old/$file" ]; then
                    mkdir -p output/old_files/$(dirname "$file")
                    cp "workspace_old/$file" "output/old_files/$file"
                  fi
                  if [ -f "workspace_new/$file" ]; then
                    mkdir -p output/new_files/$(dirname "$file")
                    cp "workspace_new/$file" "output/new_files/$file"
                  fi
                done < changed_files.txt

                echo '✅ Old and new files ready inside output/ folder.'
                '''
            }
        }

        stage('Archive Outputs') {
            steps {
                archiveArtifacts artifacts: 'output/**', fingerprint: true
            }
        }
    }
}
