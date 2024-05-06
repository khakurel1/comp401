<script>
	import Sidebar from '$components/Sidebar.svelte';
</script>

<div class="relative w-full min-h-screen">
	<Sidebar />
	<div class="relative md:ml-56 bg-blueGray-100">
		<slot />
	</div>
</div>
