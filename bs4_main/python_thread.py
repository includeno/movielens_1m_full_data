import concurrent.futures

# 定义一个函数，模拟执行某个任务
def do_some_work(arg):
    print(f"Working on {arg}")
    return f"The result of {arg} is {arg * 2}"

# 创建一个线程池，指定最大线程数为 3
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    # 定义一组任务列表
    args = [1, 2, 3, 4, 5]

    # 提交任务到线程池，并获取对应的 Future 对象
    futures = [executor.submit(do_some_work, arg) for arg in args]

    # 遍历 Future 对象，获取执行结果
    for future in concurrent.futures.as_completed(futures):
        try:
            result = future.result()
        except Exception as e:
            print(f"An error occurred: {e}")
        else:
            print(f"The result is {result}")