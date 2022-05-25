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
        sh 'docker run dxa4481/trufflehog --json https://github.com/Narendran36/webapp.git > trufflehog || true'
        sh 'cat trufflehog'
      }
    }
    
    stage ('Source Composition Analysis'){
      steps {
        sh 'rm owasp* || true'
        sh 'wget "https://raw.githubusercontent.com/Narendran36/webapp/master/owasp-dependency-check.sh"'
        sh 'chmod +x owasp-dependency-check.sh'
        sh 'bash owasp-dependency-check.sh'
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
          sh 'scp -o StrictHostKeyChecking=no target/*.war ubuntu@3.110.163.100:/prod/apache-tomcat-9.0.63/webapps/webapp.war'
        }
      }
    }
    
    stage ('Port Scan'){
      steps {
        sh 'rm nmap* || true'
        sh 'docker run --rm -v "$(pwd)":/data uzyexe/nmap -sS -sV -oX nmap 3.110.163.100'
        sh 'cat nmap'
      }
    }
    
    stage ('DAST') {
      steps {
        sshagent(['zap']) {
          sh 'ssh -o StrictHostKeyChecking=no ubuntu@65.1.111.137 "docker run -t owasp/zap2docker-stable zap-baseline.py -t http://3.110.163.100:8080/webapp/" || true'
        }
      }
    }
    
    stage ('Nikto Scan') {
		    steps {
			sh 'rm nikto-output.xml || true'
			sh 'docker pull frapsoft/nikto:latest'
			sh 'docker run --user $(id -u):$(id -g) --rm -v $(pwd):/report -i frapsoft/nikto:latest -h 3.110.163.100 -p 8080 -output /report/nikto-output.xml'
			sh 'cat nikto-output.xml'   
		    }
	    }
    
    stage ('SSL Checks') {
		    steps {
			sh 'pip install sslyze'
			sh 'python -m sslyze --regular 3.110.163.100:8080 --json_out sslyze-output.json'
			sh 'cat sslyze-output.json'
		    }
	    }
    
  }
}
