<script setup>
</script>
<template>
    <div class="page-wrapper">
        <div class="content">
            <img src="@/assets/steam-headless-logo.png" id="logo" />
            <h1 class="page-title">Steam Headless</h1>
        </div>

    </div>
</template>

<style scoped>
.page-wrapper {
    display: flex;
    padding-top: 30vh;
    justify-content: flex-start;
    align-items: center;
    background-color: transparent;
    background-image: url("@/assets/background.jpg");
    background-size: cover;
    background-position: center;
    width: 100vw;
    height: 100vh;
    margin-top: 0;
}
.page-title {
    text-align: center;
    align-self: center;
    font-size: 45px;
    font-weight: 700;
}
.content {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1rem 5rem;
    border-radius: 20px;
}
#logo {
    height: 6rem;
    width: 6rem;
    box-shadow: 0px 50px 250px 300px #102a43b0;
    background-color:#102a43b0;
}

@media screen and (max-width: 700px) {
    #logo {
        height: 5rem;
        width: 5rem;
    }
    .page-title {
        font-size: 30px;
    }
}
</style>