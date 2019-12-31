node {
 
 //commit_id will be also the tag for docker registry
 def commit_id
 
 // Checkout and get the commit_id
 stage('Preparation') {
  checkout scm
  sh "git rev-parse --short HEAD > .git/commit-id"
  commit_id = readFile('.git/commit-id').trim()
 }
 
 stage('test') {
  // Build the docker image and run tests
  // If needed you can define a Dockerfile suitable for testing
  def myTestContainer = docker.build("test-python", "--no-cache -f ./dockerfiles/Dockerfile .")
  myTestContainer.inside {
   sh 'python ./tests/python_tests.py'
  }
 }
 
 stage('push to docker registry') {
  // build and push to docker registry
  docker.withRegistry('https://index.docker.io/v1/', 'dockerhub') {
   def app = docker.build("kpat/python-pipeline-demo:${commit_id}", "--no-cache -f ./dockerfiles/Dockerfile .").push()
  }
 }       
 
}
