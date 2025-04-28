pipeline {
    agent any

    parameters {
        string(name: 'COMPARISON_SERVER_URL', defaultValue: 'http://172.25.90.18:9000/getFiles', description: 'URL of the comparison service')
    }

    environment {
        OLD_BRANCH = 'main'
        NEW_BRANCH = 'pritesh/test/jenkins'
        
    }

    stages {
        stage('Clone Repository') {
            steps {
                sh 'rm -rf workspace_old workspace_new output || true'
                sh 'mkdir workspace_old workspace_new output'

                echo "📦 Cloning ${OLD_BRANCH} branch (OLD files)..."
                dir('workspace_old') {
                    git branch: "${OLD_BRANCH}", url: 'https://github.com/Pritesh-Kadam-10/Demo.git'
                }

                echo "📦 Cloning ${NEW_BRANCH} branch (NEW files)..."
                dir('workspace_new') {
                    git branch: "${NEW_BRANCH}", url: 'https://github.com/Pritesh-Kadam-10/Demo.git'
                }
            }
        }

        stage('Prepare Changed Files') {
            steps {
                echo '🛠 Identifying changed files...'
                script {
                    dir('workspace_new') {
                        sh 'git fetch origin ${OLD_BRANCH}'
                    }

                    def changedFiles = sh(script: """
                        cd workspace_new
                        git diff --name-only origin/${OLD_BRANCH}..origin/${NEW_BRANCH}
                    """, returnStdout: true).trim()

                    if (changedFiles) {
                        echo "✅ Files changed:\n${changedFiles}"

                        for (file in changedFiles.split("\\n")) {
                            file = file.trim()
                            if (file) {
                                sh """
                                    mkdir -p "output/old_files/\$(dirname \"${file}\")"
                                    mkdir -p "output/new_files/\$(dirname \"${file}\")"
                                    if [ -f "workspace_old/${file}" ]; then cp -r "workspace_old/${file}" "output/old_files/${file}"; fi
                                    if [ -f "workspace_new/${file}" ]; then cp -r "workspace_new/${file}" "output/new_files/${file}"; fi
                                """
                            }
                        }
                        echo '✅ Old and new files are prepared inside output/ folder.'
                    } else {
                        echo '⚠️ No files changed between the branches!'
                        sh 'mkdir -p output/empty'
                        sh 'echo "No changes detected." > output/empty/info.txt'
                    }
                }
            }
        }

        stage('Archive Outputs') {
            steps {
                archiveArtifacts artifacts: 'output/**', allowEmptyArchive: true
            }
        }

        stage('Send Files for Comparison') {
            steps {
                script {
                    echo '🚀 Zipping and sending files to comparison service...'
                    sh """
                        cd output
                        zip -r old_files.zip old_files || echo "No old files to zip"
                        zip -r new_files.zip new_files || echo "No new files to zip"
                        cd ..

                        curl -X POST ${params.COMPARISON_SERVER_URL} \
                        -F "oldFiles=@output/old_files.zip" \
                        -F "newFiles=@output/new_files.zip"
                    """
                }
            }
        }
    }
}
