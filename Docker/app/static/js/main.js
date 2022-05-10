function copy_refresh_token() {
    const copyText = document.getElementById("refresh_token").textContent;
    const textArea = document.createElement('textarea');
    textArea.textContent = copyText;
    document.body.append(textArea);
    textArea.select();
    document.execCommand("copy");
    refresh_button.innerText = "Password copiada!";
    textArea.remove();
}

function copy_id_user(event) {
  const copyText = document.getElementById("id_user").textContent;
  const textArea = document.createElement('textarea');
  textArea.textContent = copyText;
  document.body.append(textArea);
  textArea.select();
  document.execCommand("copy");
  id_button.innerText = "ID copiada!";
  textArea.remove();
} 

document.getElementById('refresh_button').addEventListener('click', copy_refresh_token);
document.getElementById('id_button').addEventListener('click', copy_id_user);
document.getElementById('id_button').addEventListener('touchstart', copy_id_user, false);
document.querySelector(".parent").addEventListener("click", copy_id_user)
document.querySelector(".parent").addEventListener("touchstart", copy_id_user, false)