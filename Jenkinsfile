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
  }
}
