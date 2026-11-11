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
                script {
                    env.PY = isUnix() ? 'python3' : 'python'
                    env.VPY = isUnix() ? '.ci-venv/bin/python' : '.ci-venv\\Scripts\\python'
                }
                echo "빌드 ${env.BUILD_NUMBER} - 커밋 ${env.GIT_COMMIT}"
            }
        }
        stage('Setup') {       
            steps {            
                // 가상환경
                // sh "python3 -m venv .ci-venv"      
                // bat "python -m venv .ci-venv"        
                runCmd "${env.PY} -m venv .ci-venv"       
                runCmd "${env.VPY} -m pip install -q -r requirements.txt pytest pytest-html"
            }
        }
        stage('Syntax Check') {       
            steps {            
                // py_complie app.py   deploy.py <- 문법 적용
                runCmd "${env.VPY} -m py_compile app.py deploy.py"       
                sleep time:3, unit:'SECONDS'
            }
        }
        stage('Data Check'){
            steps {
                runCmd "${env.VPY} -m pytest -v tests/test_data.py --junitxml=reports/junit.xml --html=reports/report.html --self-contained-html"
                sleep time:3, unit:'SECONDS'
            }
        }
        stage('API Test') {       
            steps {            
                // pytest 실행
                runCmd "${env.VPY} -m pytest -v tests/test_api.py --junitxml=reports/junit.xml --html=reports/report.html --self-contained-html"
                sleep time:3, unit:'SECONDS'
            }
        }
        stage('Deploy') {       
            steps {            
                runCmd "${env.VPY} deploy.py"
            }
        }
    }
    
    post {                     // 모든 단계가 끝난 뒤
       always {          // 성공 · 실패와 관계없이
            // junit
            junit allowEmptyResults:true, testResults:'reports/*.xml'
            
            // html publish
            publishHTML(target:[
                reportDir: 'reports',
                reportFiles: 'data.html, report.html',
                reportName: 'pytest report',
                keepAll: true,
                alwaysLinkToLastBuild: true,
                allowMissing: true
            ])


            // 이메일 전송
            // slack 전송
        }
        // failure { ... }        // 실패했을 때만
    }
}