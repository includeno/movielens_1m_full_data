# 使用JavaScript使页面滑到底部
script='window.scrollTo(0, document.body.scrollHeight);'

def jump_to_bottom(count=1,time_to_sleep=0):
    if(count==1):
        return script
    st=""
    st=st+f"""let count={count};\nlet time={time_to_sleep};\n"""
    st=st+"""function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
async function demo() {
    for (let i = 0; i < count; i++) {
        window.scrollTo(0, document.body.scrollHeight);
        await sleep(time);
    }
}
demo();"""
    return st

def jump_to_bottom2(count=1,time_to_sleep=0):
    if(count==1):
        return script
    st=""
    st=st+f"""let count={count};\nlet time={time_to_sleep};\n"""
    st=st+"""function demo() {
    for (let i = 0; i < count; i++) {
        window.scrollTo(0, document.body.scrollHeight);
        setTimeout(null,time );
    }
}
demo();"""
    return st
s=jump_to_bottom2(count=100,time_to_sleep=1000)
print(s)