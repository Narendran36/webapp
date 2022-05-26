pipeline {
  agent any
  tools {
    maven 'Maven'
  }
  stages {
    stage ('Initialize') {
      steps {
        sh '''
          echo "PATH = ${PATH}"
          echo "M2_HOME = ${M2_HOME}"
          '''
      }
    }
    
    stage ('Check-Git-Secrets'){
      steps {
        sh 'rm trufflehog || true'
        sh 'docker run --rm dxa4481/trufflehog --json https://github.com/Narendran36/webapp.git > trufflehog || true'
        sh 'cat trufflehog'
      }
    }
    
    stage ('Source Composition Analysis'){
      steps {
        sh 'rm owasp* || true'
        sh 'wget "https://raw.githubusercontent.com/Narendran36/webapp/master/owasp-dependency-check.sh"'
        sh 'chmod +x owasp-dependency-check.sh'
        sh 'bash owasp-dependency-check.sh || true'
        sh 'cat /var/lib/jenkins/workspace/WebApp-CICD-Pipeline/odc-reports/dependency-check-report.xml'
      }
    }
    
    stage ('SAST') {
      steps {
        withSonarQubeEnv('sonar'){
          sh 'mvn sonar:sonar'
          sh 'cat target/sonar/report-task.txt'
        }
      }
    }
    
    stage ('Build') {
      steps {
      sh 'mvn clean package' 
      }
    }
    
    stage ('Deploy-to-Tomcat') {
      steps {
        sshagent(['tomcat']) {
          sh 'scp -o StrictHostKeyChecking=no target/*.war ubuntu@65.2.63.134:/prod/apache-tomcat-9.0.63/webapps/webapp.war'
        }
      }
    }
    
    stage ('Port Scan'){
      steps {
        sh 'rm nmap* || true'
        sh 'docker run --rm -v "$(pwd)":/data uzyexe/nmap -sS -sV -oX nmap 65.2.63.134'
        sh 'cat nmap'
      }
    }
    
    stage ('DAST') {
      steps {
	sh 'rm zap-report.xml || true'
	sh 'docker run --user root --rm -v $(pwd):/zap/wrk/:rw -t ictu/zap2docker-weekly zap-baseline.py -I -t http://65.2.63.134:8080/webapp/ -x zap-report.xml || true'
        sh 'cat zap-report.xml'
      }
    }
    
    stage ('Nikto Scan') {
		    steps {
			sh 'rm nikto-output.xml || true'
			sh 'docker pull secfigo/nikto:latest'
			sh 'docker run --user $(id -u):$(id -g) --rm -v $(pwd):/report -i secfigo/nikto:latest -h 65.2.63.134 -p 8080 -output /report/nikto-output.xml'
			sh 'cat nikto-output.xml'
		    }
	    }
    
    stage ('SSL Checks') {
		    steps {
			sh 'pip install sslyze'
			sh 'python3 -m sslyze 65.2.63.134:8080 --json_out sslyze-output.json || true'
			sh 'cat sslyze-output.json'
		    }
	    }
    
  }
}
