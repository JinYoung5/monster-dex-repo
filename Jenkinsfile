def runCmd(String cmd) {
    if (isUnix()) {
        sh cmd
    } else {
        bat cmd
    }
}

pipeline {

    agent any

    triggers {
        pollSCM('H/2 * * * *') // 2분마다 실행
    }
        
    stages {                   
        stage('Prepare') {         
            steps {           
                script{
                    env.PY = isUnix() ? 'python3' : 'python'
                    env.VPY = isUnix() ? '.ci-venv/bin/python' : '.ci-venv\\Scripts\\python'
                }
                echo "빌드 ${env.BUILD_NUMBER} - 커밋 ${env.GIT_COMMIT}"
            }
        }
    }

    stages {                   
        stage('Setup') {
            steps {
                runCmd "${env.PY} -m venv .ci-venv"
                runCmd "${env.VPY} -m pip install -q -r requirements.txt pytest"
            }
        }
    }

    stages {                   
        stage('Syntax Check') {
            steps {
                runCmd "${env.PY} -m py_complie app.py deploy.py"
            }
        }
    }

    stages {                   
        stage('Test') {
            steps {
                runCmd "${env.PY} -m pytest -v"
            }
        }
    }

    stages {                   
        stage('Deploy') {
            steps {
                runCmd "${env.PY} deploy.py"
            }
        }
    }

    post {                     // 모든 단계가 끝난 뒤
        always { ... }         // 성공 · 실패와 관계없이
        failure { ... }        // 실패했을 때만
    }
}